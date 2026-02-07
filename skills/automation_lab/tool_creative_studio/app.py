import streamlit as st
import time
import tempfile
import os
from io import BytesIO
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# --- Lazy Imports ---
# Isso previne que o app trave na inicialização se uma lib demorar pra carregar
def get_pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont

def get_requests():
    import requests
    return requests

def get_rembg():
    from rembg import remove
    return remove

def get_moviepy():
    try:
        from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip
        return True, ImageClip, TextClip, CompositeVideoClip, AudioFileClip
    except ImportError:
        return False, None, None, None, None

@st.cache_resource
def get_gemini():
    import google.generativeai as genai
    return genai

def get_openai():
    from openai import OpenAI
    return OpenAI

def generate_script_openrouter(topic, model="openai/gpt-3.5-turbo"):
    OpenAI = get_openai()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return "Erro: Chave API OpenRouter não configurada."
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um roteirista criativo e poético."},
                {"role": "user", "content": f"Crie um roteiro curto e inspirador (max 100 caracteres) para um vídeo sobre: {topic}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro OpenRouter: {str(e)}"

# --- Configuração Inicial ---
st.set_page_config(page_title="O Estúdio Onírico", page_icon="🎬", layout="wide")
st.title("🎬 O Estúdio Onírico: Mesa de Regência")
st.markdown("> *\"Você descreve pontos, eu ligo as arestas.\"*")

# --- Gerenciamento de Estado ---
if 'workspace' not in st.session_state:
    st.session_state['workspace'] = {
        'image_raw': None,
        'image_processed': None,
        'source_name': None
    }

Image, ImageDraw, ImageFont = get_pil()

def set_image(img, name):
    st.session_state['workspace']['image_raw'] = img
    st.session_state['workspace']['image_processed'] = None 
    st.session_state['workspace']['source_name'] = name
    st.toast(f"Imagem '{name}' enviada para o Ateliê!", icon="🎨")

# --- Funções Auxiliares ---
def generate_script_gemini(topic, model_name="gemini-1.5-flash"):
    try:
        genai = get_gemini()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Erro: Configure a API Key do Gemini."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"Crie um roteiro curto (max 30s) e inspirador sobre: {topic}. Retorne APENAS o texto da narração.")
        return response.text
    except Exception as e:
        return f"Erro Gemini: {e}"

def generate_audio_elevenlabs(text, voice_id="21m00Tcm4TlvDq8ikWAM"): # Voice: Rachel
    requests = get_requests()
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return None, "Erro: Chave API ElevenLabs não configurada."
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            output_path = tempfile.mktemp(suffix=".mp3")
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path, None
        else:
            return None, f"Erro ElevenLabs: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Erro Requisição: {str(e)}"

def create_video_from_image(pil_image, text, duration, audio_path=None):
    available, ImageClip, _, _, AudioFileClip = get_moviepy()
    if not available:
        return None

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        pil_image.save(f.name)
        img_path = f.name
    
    # Desenhar texto na imagem
    try:
        font = ImageFont.truetype("Arial", 40)
    except:
        font = ImageFont.load_default()
        
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f_text:
        pil_image_with_text = pil_image.copy()
        draw = ImageDraw.Draw(pil_image_with_text)
        draw.text((50, 50), text, fill="white") 
        pil_image_with_text.save(f_text.name)
        img_text_path = f_text.name
        
    final_clip = ImageClip(img_text_path).set_duration(duration)
    
    if audio_path:
        try:
            audio_clip = AudioFileClip(audio_path)
            # Corta o áudio se for maior que a duração do vídeo, ou loopa se for menor (aqui vamos cortar)
            if audio_clip.duration > duration:
                audio_clip = audio_clip.subclip(0, duration)
            final_clip = final_clip.set_audio(audio_clip)
        except Exception as e:
            st.error(f"Erro ao processar áudio: {e}")

    final_clip = final_clip.set_fps(24)
    
    output_path = tempfile.mktemp(suffix=".mp4")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac" if audio_path else None)
    
    os.remove(img_path)
    os.remove(img_text_path)
    
    return output_path

def render_card_grid(key_prefix, options, cols=3):
    """
    Renderiza uma grade de cartões selecionáveis.
    options: lista de dicts com chaves: id, title, caption, description, image, pros, cons
    """
    columns = st.columns(cols)
    selected_value = None
    
    for idx, opt in enumerate(options):
        col = columns[idx % cols]
        with col:
            with st.container(border=True):
                if opt.get("image"):
                    st.image(opt["image"], use_container_width=True)
                st.write(f"### {opt['title']}")
                if opt.get("caption"):
                    st.caption(opt["caption"])
                if opt.get("description"):
                    st.markdown(opt["description"])
                
                if opt.get("pros") or opt.get("cons"):
                    st.divider()
                    if opt.get("pros"):
                        st.markdown(f"**✅ Prós:**\n{opt['pros']}")
                    if opt.get("cons"):
                        st.markdown(f"**❌ Contras:**\n{opt['cons']}")
                
                if st.button(f"Selecionar {opt['title']}", key=f"btn_{key_prefix}_{opt['id']}", use_container_width=True):
                    selected_value = opt['id']
                    
    return selected_value


# --- Sidebar ---
with st.sidebar:
    st.header("🎛️ Controles")
    
    # --- Configuração de Chaves (API Keys) ---
    with st.expander("🔑 Chaves de API", expanded=False):
        # Carrega valores atuais (prioridade: session_state > env var)
        gemini_key = st.session_state.get('GEMINI_API_KEY', os.environ.get("GEMINI_API_KEY", ""))
        eleven_key = st.session_state.get('ELEVENLABS_API_KEY', os.environ.get("ELEVENLABS_API_KEY", ""))
        openai_key = st.session_state.get('OPENAI_API_KEY', os.environ.get("OPENAI_API_KEY", ""))
        openrouter_key = st.session_state.get('OPENROUTER_API_KEY', os.environ.get("OPENROUTER_API_KEY", ""))
        
        with st.form("api_keys_form"):
            new_gemini_key = st.text_input("Gemini API Key", value=gemini_key, type="password")
            new_eleven_key = st.text_input("ElevenLabs API Key", value=eleven_key, type="password")
            new_openai_key = st.text_input("OpenAI API Key", value=openai_key, type="password")
            new_openrouter_key = st.text_input("OpenRouter API Key", value=openrouter_key, type="password")
            
            submitted = st.form_submit_button("💾 Salvar e Persistir")
            
            if submitted:
                # Atualiza variáveis de ambiente na memória
                os.environ["GEMINI_API_KEY"] = new_gemini_key
                os.environ["ELEVENLABS_API_KEY"] = new_eleven_key
                os.environ["OPENAI_API_KEY"] = new_openai_key
                os.environ["OPENROUTER_API_KEY"] = new_openrouter_key
                
                # Atualiza session state para manter a UI sincronizada
                st.session_state['GEMINI_API_KEY'] = new_gemini_key
                st.session_state['ELEVENLABS_API_KEY'] = new_eleven_key
                st.session_state['OPENAI_API_KEY'] = new_openai_key
                st.session_state['OPENROUTER_API_KEY'] = new_openrouter_key
                
                # Salva no arquivo .env para persistência
                try:
                    env_content = f"""GEMINI_API_KEY={new_gemini_key}
ELEVENLABS_API_KEY={new_eleven_key}
OPENAI_API_KEY={new_openai_key}
OPENROUTER_API_KEY={new_openrouter_key}
"""
                    with open(".env", "w") as f:
                        f.write(env_content)
                    st.success("Chaves salvas em .env com sucesso!")
                    st.toast("Chaves de API atualizadas!", icon="🔐")
                except Exception as e:
                    st.error(f"Erro ao salvar .env: {e}")

    # --- Debug Mode ---
    if 'debug_mode' not in st.session_state:
        st.session_state['debug_mode'] = False
        
    debug_mode = st.toggle("🐞 Modo Debug (Mostrar Logs)", value=st.session_state['debug_mode'])
    st.session_state['debug_mode'] = debug_mode
    
    if debug_mode:
        st.caption("Logs técnicos serão exibidos na tela.")

        # --- Botão de Teste de Conexão ---
        if st.button("📡 Testar Conexões"):
            with st.status("Verificando credenciais...", expanded=True) as status:
                
                # Teste Gemini
                if gemini_key:
                    st.write("🔹 Testando Gemini...")
                    try:
                        genai = get_gemini()
                        genai.configure(api_key=gemini_key)
                        genai.list_models() # Call leve para verificar auth
                        st.success("Gemini: Conectado!")
                    except Exception as e:
                        st.error(f"Gemini: Falha ({str(e)})")
                else:
                    st.warning("Gemini: Chave não definida")

                # Teste OpenAI
                if openai_key:
                    st.write("🔹 Testando OpenAI...")
                    try:
                        OpenAI = get_openai()
                        client = OpenAI(api_key=openai_key)
                        client.models.list()
                        st.success("OpenAI: Conectado!")
                    except Exception as e:
                        st.error(f"OpenAI: Falha ({str(e)})")
                else:
                    st.warning("OpenAI: Chave não definida")

                # Teste OpenRouter
                if openrouter_key:
                    st.write("🔹 Testando OpenRouter...")
                    try:
                        OpenAI = get_openai()
                        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_key)
                        client.models.list()
                        st.success("OpenRouter: Conectado!")
                    except Exception as e:
                        st.error(f"OpenRouter: Falha ({str(e)})")
                else:
                    st.warning("OpenRouter: Chave não definida")

                # Teste ElevenLabs
                if eleven_key:
                    st.write("🔹 Testando ElevenLabs...")
                    try:
                        requests = get_requests()
                        headers = {"xi-api-key": eleven_key}
                        resp = requests.get("https://api.elevenlabs.io/v1/user", headers=headers)
                        if resp.status_code == 200:
                            st.success("ElevenLabs: Conectado!")
                        else:
                            st.error(f"ElevenLabs: Falha ({resp.status_code})")
                    except Exception as e:
                        st.error(f"ElevenLabs: Erro ({str(e)})")
                else:
                    st.warning("ElevenLabs: Chave não definida")
                
                status.update(label="Teste Completo!", state="complete", expanded=True)

    mode = st.selectbox("Modo de Operação", ["Exploração Visual", "Ateliê de Edição", "Montagem de Cena"])
    
    st.divider()
    st.caption("Status do Workspace")
    if st.session_state['workspace']['image_raw']:
        st.success("Imagem: Carregada")
    else:
        st.warning("Imagem: Pendente")

# --- Lógica dos Modos ---

if mode == "Exploração Visual":
    st.subheader("🔍 Caçador de Imagens")
    
    st.write("Sugestões:")
    col_sug1, col_sug2, col_sug3 = st.columns(3)
    if col_sug1.button("🎒 Uniformes Escolares"):
        st.session_state['query_input'] = "Uniformes escolares crianças felizes escola"
    if col_sug2.button("🏙️ Cidade Cyberpunk"):
        st.session_state['query_input'] = "Cidade futurista neon chuva"
    if col_sug3.button("☕ Café da Manhã"):
        st.session_state['query_input'] = "Café da manhã saudável frutas"

    default_query = st.session_state.get('query_input', "Uma paisagem onírica")
    query = st.text_input("O que sua mente vê?", default_query)
    
    # --- Source Selection Logic ---
    if 'visual_source_selection' not in st.session_state:
        st.session_state['visual_source_selection'] = None

    selected_source = st.session_state['visual_source_selection']

    if selected_source is None:
        st.markdown("### 🎨 Escolha sua Fonte Visual")
        
        source_options = [
            {
                "id": "pollinations",
                "title": "Pollinations",
                "caption": "Criatividade Ilimitada",
                "description": "Geração via modelos open-source (Flux, SDXL).",
                "image": "https://picsum.photos/seed/pollinations/300/150",
                "pros": "- Gratuito e Ilimitado\n- Sem chave\n- Rápido",
                "cons": "- Menor precisão"
            },
            {
                "id": "dalle",
                "title": "OpenAI DALL-E",
                "caption": "Precisão e Realismo",
                "description": "O estado da arte em seguir instruções.",
                "image": "https://images.unsplash.com/photo-1617791160505-6f00504e3519?w=300&h=150&fit=crop",
                "pros": "- Alta fidelidade\n- Fotorealismo",
                "cons": "- Pago"
            },
            {
                "id": "gemini",
                "title": "Google Gemini",
                "caption": "Imagen 3 (SOTA)",
                "description": "Alta fidelidade e melhor renderização de texto.",
                "image": "https://picsum.photos/seed/gemini/300/150",
                "pros": "- Alta Qualidade\n- Texto legível",
                "cons": "- Preview/Beta"
            },
            {
                "id": "openrouter",
                "title": "OpenRouter",
                "caption": "Hub de Modelos",
                "description": "Acesso a múltiplos modelos (Stable Diffusion, etc).",
                "image": "https://picsum.photos/seed/openrouter/300/150?grayscale", 
                "pros": "- Variedade\n- Modelos de ponta",
                "cons": "- Configuração complexa"
            },
            {
                "id": "picsum",
                "title": "Picsum",
                "caption": "Fotos Reais Aleatórias",
                "description": "Banco de imagens reais para placeholder.",
                "image": "https://picsum.photos/300/150",
                "pros": "- Fotos reais\n- Instantâneo",
                "cons": "- Aleatório"
            }
        ]
        
        sel = render_card_grid("source", source_options, cols=4)
        if sel:
            st.session_state['visual_source_selection'] = sel
            st.rerun()

    else:
        # Show selected source UI
        col_header, col_btn = st.columns([4,1])
        with col_header:
            if selected_source == "pollinations":
                st.info("🎨 Fonte Selecionada: **Pollinations AI** (Flux/SDXL)")
            elif selected_source == "dalle":
                st.info("🧠 Fonte Selecionada: **OpenAI DALL-E**")
            elif selected_source == "openrouter":
                st.info("⚡ Fonte Selecionada: **OpenRouter**")
            elif selected_source == "picsum":
                st.info("🎲 Fonte Selecionada: **Picsum** (Aleatório)")
        
        with col_btn:
            if st.button("🔄 Trocar Fonte"):
                st.session_state['visual_source_selection'] = None
                # Limpa seleções de modelos também
                st.session_state.pop('pollinations_model', None)
                st.session_state.pop('dalle_model', None)
                st.session_state.pop('dalle_quality', None)
                st.session_state.pop('openrouter_model', None)
                st.rerun()

        # Configuration Logic with Cards
        
        # 1. DALL-E Configuration
        dalle_model = st.session_state.get('dalle_model', "dall-e-3")
        dalle_quality = st.session_state.get('dalle_quality', "standard")
        
        if selected_source == "dalle":
            st.markdown("### ⚙️ Configuração DALL-E")
            
            # Step 1: Model Selection
            st.markdown("#### 1. Modelo")
            dalle_options = [
                {"id": "dall-e-3", "title": "DALL-E 3", "description": "Maior fidelidade ao prompt.", "image": "https://picsum.photos/seed/dalle3/300/100"},
                {"id": "dall-e-2", "title": "DALL-E 2", "description": "Mais rápido e econômico.", "image": "https://picsum.photos/seed/dalle2/300/100"}
            ]
            sel_dalle = render_card_grid("dalle_model", dalle_options, cols=2)
            if sel_dalle:
                st.session_state['dalle_model'] = sel_dalle
                st.rerun()
            st.caption(f"Selecionado: **{dalle_model}**")

            # Step 2: Quality (only for DALL-E 3)
            if dalle_model == "dall-e-3":
                st.markdown("#### 2. Qualidade")
                qual_options = [
                    {"id": "standard", "title": "Standard", "description": "Qualidade padrão.", "image": "https://picsum.photos/seed/std/300/100?grayscale"},
                    {"id": "hd", "title": "HD", "description": "Alta definição (mais caro).", "image": "https://picsum.photos/seed/hd/300/100"}
                ]
                sel_qual = render_card_grid("dalle_quality", qual_options, cols=2)
                if sel_qual:
                    st.session_state['dalle_quality'] = sel_qual
                    st.rerun()
                st.caption(f"Selecionado: **{dalle_quality}**")

        # 2. Pollinations Configuration
        pollinations_model = st.session_state.get('pollinations_model', "flux")
        if selected_source == "pollinations":
            st.markdown("### ⚙️ Configuração Pollinations")
            
            poll_options = [
                {"id": "flux", "title": "Flux", "description": "Novo modelo state-of-the-art open source.", "image": "https://image.pollinations.ai/prompt/hyperrealistic%20portrait?model=flux&width=300&height=100&nologo=true"},
                {"id": "turbo", "title": "Turbo", "description": "Geração ultra-rápida.", "image": "https://image.pollinations.ai/prompt/fast%20car%20neon?model=turbo&width=300&height=100&nologo=true"},
                {"id": "midjourney", "title": "Midjourney Style", "description": "Estilo artístico característico.", "image": "https://image.pollinations.ai/prompt/fantasy%20landscape?model=midjourney&width=300&height=100&nologo=true"},
                {"id": "diffusion", "title": "Stable Diffusion", "description": "Clássico e versátil.", "image": "https://image.pollinations.ai/prompt/robot?model=diffusion&width=300&height=100&nologo=true"}
            ]
            sel_poll = render_card_grid("poll_model", poll_options, cols=4)
            if sel_poll:
                st.session_state['pollinations_model'] = sel_poll
                st.rerun()
            st.caption(f"Selecionado: **{pollinations_model}**")

        # 3. Gemini Configuration
        if selected_source == "gemini":
            st.markdown("### ⚙️ Configuração Gemini")
            st.info("Utilizando modelo **Imagen 3** (se disponível na sua API Key).")
            st.caption("Nota: A geração de imagens via API do Gemini ainda está em Beta e pode não estar disponível em todas as regiões/chaves.")

        # 4. OpenRouter Configuration
        openrouter_model = st.session_state.get('openrouter_model', "google/gemini-2.0-pro-exp-02-05:free")
        if selected_source == "openrouter":
            st.markdown("### ⚙️ Configuração OpenRouter")
            
            # Button to list models
            if st.button("🔍 Listar Modelos Disponíveis (API Check)"):
                requests = get_requests() # Fix: Import requests locally
                api_key = os.environ.get("OPENROUTER_API_KEY") or st.session_state.get("OPENROUTER_API_KEY")
                if not api_key:
                    st.error("Configure a API Key do OpenRouter primeiro.")
                else:
                    try:
                        with st.spinner("Buscando modelos..."):
                            resp = requests.get("https://openrouter.ai/api/v1/models")
                            if resp.status_code == 200:
                                data = resp.json()
                                models = data.get('data', [])
                                # Filter likely image models
                                keywords = ['image', 'vision', 'diffusion', 'stability', 'flux', 'dall', 'mj']
                                img_models = [m for m in models if any(k in m.get('id','').lower() for k in keywords)]
                                
                                if img_models:
                                    st.success(f"Encontrados {len(img_models)} modelos de imagem:")
                                    for m in img_models:
                                        st.code(f"{m['id']}")
                                else:
                                    st.warning("Nenhum modelo óbvio de imagem encontrado (busquei por keywords).")
                                    st.write("Exibindo primeiros 10 modelos encontrados (verifique se algum serve):")
                                    for m in models[:10]:
                                        st.code(m['id'])
                            else:
                                st.error(f"Erro ao listar modelos: {resp.status_code}")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")

            or_options = [
                {"id": "custom", "title": "Digitar ID Manualmente", "description": "Consulte a lista acima para IDs válidos.", "image": "https://picsum.photos/seed/custom/300/100?grayscale"},
                {"id": "google/gemini-2.0-pro-exp-02-05:free", "title": "Gemini 2.0 Pro Exp (Free)", "description": "Modelo experimental mais recente.", "image": "https://picsum.photos/seed/gemini/300/100"},
            ]
            sel_or = render_card_grid("or_model", or_options, cols=2)
            if sel_or:
                st.session_state['openrouter_model'] = sel_or
                st.rerun()
            
            if openrouter_model == "custom":
                openrouter_model = st.text_input("Digite o ID do Modelo OpenRouter", value="google/gemini-2.0-pro-exp-02-05:free")
            else:
                st.caption(f"Selecionado: **{openrouter_model}**")

        st.caption("ℹ️ Nota: As chaves Gemini e OpenRouter são utilizadas para **Geração de Roteiro** na aba 'Montagem de Cena'.")

        if st.button("🚀 Buscar / Gerar Imagem", type="primary", use_container_width=True):
            requests = get_requests()
            debug = st.session_state.get('debug_mode', False)
            
            with st.spinner("Sintonizando frequências visuais..."):
                
                if selected_source == "dalle":
                    api_key = os.environ.get("OPENAI_API_KEY")
                    if not api_key:
                        st.error("Chave OpenAI não configurada! Adicione na sidebar.")
                    else:
                        try:
                            OpenAI = get_openai()
                            client = OpenAI(api_key=api_key)
                            
                            # Retrieve params from session state or defaults
                            model = st.session_state.get('dalle_model', "dall-e-3")
                            quality = st.session_state.get('dalle_quality', "standard")
                            
                            params = {
                                "model": model,
                                "prompt": query,
                                "n": 1,
                            }
                            
                            if model == "dall-e-3":
                                params["size"] = "1024x1024"
                                params["quality"] = quality
                            else:
                                params["size"] = "1024x1024" # DALL-E 2 standard

                            if debug: st.write(f"🐞 DALL-E Params: {params}")

                            response = client.images.generate(**params)
                            image_url = response.data[0].url
                            if debug: st.write(f"🐞 DALL-E URL: {image_url}")
                            
                            # Proxy: Download server-side to avoid CORS/ORB issues
                            resp = requests.get(image_url)
                            img = Image.open(BytesIO(resp.content))
                            st.image(img, caption=f"DALL-E ({model}) Generation")
                            
                            set_image(img, f"DALL-E: {query[:20]}...")
                            st.success("Imagem gerada e carregada no workspace!")
                            
                        except Exception as e:
                            st.error(f"Erro OpenAI: {e}")
                            if debug: st.exception(e)

                elif selected_source == "gemini":
                    api_key = os.environ.get("GEMINI_API_KEY")
                    if not api_key:
                        st.error("Chave Gemini não configurada! Adicione na sidebar.")
                    else:
                        try:
                            genai = get_gemini()
                            genai.configure(api_key=api_key)
                            
                            if debug: st.write("🐞 Inicializando Imagen 3...")
                            
                            # Tenta acessar o modelo de imagem (requer google-generativeai >= 0.8.0 ou pacote google-genai)
                            if hasattr(genai, 'ImageGenerationModel'):
                                imagen_model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                                response = imagen_model.generate_images(
                                    prompt=query,
                                    number_of_images=1,
                                )
                                
                                if debug: st.write(f"🐞 Response type: {type(response)}")
                                
                                if response.images:
                                    img = response.images[0] # PIL Image
                                    st.image(img, caption="Gemini Imagen 3")
                                    set_image(img, f"Gemini: {query[:20]}...")
                                    st.success("Imagem gerada com Gemini!")
                                else:
                                    st.error("Nenhuma imagem retornada.")
                            else:
                                st.warning("⚠️ Geração de Imagem Nativa (Imagen 3) indisponível nesta versão da lib.")
                                st.markdown("A API do Gemini para imagens mudou recentemente. Para gerar imagens **AGORA**, use o **Pollinations** (Grátis/Ilimitado) ou **OpenRouter**.")
                                # Fallback graceful
                                if st.button("🔄 Tentar com Pollinations (Backup)"):
                                    st.session_state['visual_source_selection'] = 'pollinations'
                                    st.rerun()

                        except Exception as e:
                            st.error(f"Erro Gemini: {e}")
                            if debug: st.exception(e)

                elif selected_source == "openrouter":
                    api_key = os.environ.get("OPENROUTER_API_KEY")
                    if not api_key:
                        st.error("Chave OpenRouter não configurada! Adicione na sidebar.")
                    else:
                        try:
                            # OpenRouter Image Gen via HTTP Request
                            url = "https://openrouter.ai/api/v1/chat/completions"
                            headers = {
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "http://localhost:8501", # Required by OpenRouter
                                "X-Title": "O Estúdio Onírico"
                            }
                            
                            model = st.session_state.get('openrouter_model', "google/gemini-2.0-pro-exp-02-05:free")
                            
                            payload = {
                                "model": model,
                                "messages": [{"role": "user", "content": query}],
                            }
                            
                            if debug: 
                                st.write(f"🐞 OpenRouter Request: {url}")
                                st.json(payload)
                            
                            response = requests.post(url, headers=headers, json=payload)
                            
                            if debug: st.write(f"🐞 Status: {response.status_code}")
                            
                            if response.status_code == 200:
                                result = response.json()
                                if debug: st.json(result)
                                
                                content = result['choices'][0]['message']['content']
                                
                                # Try to find URL in content (Markdown or Raw)
                                import re
                                url_match = re.search(r'\((https?://.*?)\)', content) # Markdown link
                                if not url_match:
                                    url_match = re.search(r'(https?://[^\s]+)', content) # Raw link
                                
                                if url_match:
                                    image_url = url_match.group(1)
                                    if image_url.endswith(')'): image_url = image_url[:-1]
                                    
                                    # Proxy: Download server-side
                                    resp_img = requests.get(image_url)
                                    img = Image.open(BytesIO(resp_img.content))
                                    st.image(img, caption=f"OpenRouter ({model})")
                                    
                                    set_image(img, f"OpenRouter: {query[:20]}...")
                                    st.success("Imagem gerada e carregada!")
                                else:
                                    # Fallback: Mostra o texto se não achar imagem
                                    st.warning(f"O modelo respondeu texto, mas não encontrei URL de imagem.")
                                    st.info(f"Resposta: {content}")
                            else:
                                st.error(f"Erro OpenRouter ({response.status_code}): {response.text}")
                                
                        except Exception as e:
                            st.error(f"Erro OpenRouter: {e}")
                            if debug: st.exception(e)

                elif selected_source == "pollinations":
                    try:
                        # Pollinations API
                        import urllib.parse
                        encoded_query = urllib.parse.quote(query)
                        seed = int(time.time())
                        model = st.session_state.get('pollinations_model', "flux")
                        
                        # Tenta primeiro com o modelo específico
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_query}?width=1024&height=768&seed={seed}&nologo=true&model={model}"
                        if debug: st.write(f"🐞 URL Primária: {image_url}")
                        
                        st.info(f"Tentando gerar com Pollinations ({model})...")
                        
                        # Verifica se a URL responde
                        resp = requests.get(image_url, timeout=15)
                        if debug: st.write(f"🐞 Status Primária: {resp.status_code}")
                        
                        if resp.status_code != 200:
                            st.warning(f"Modelo '{model}' instável ({resp.status_code}). Tentando genérico...")
                            # Fallback para URL mais simples possível (sem parâmetros extras)
                            image_url = f"https://image.pollinations.ai/prompt/{encoded_query}"
                            if debug: st.write(f"🐞 URL Fallback: {image_url}")
                            resp = requests.get(image_url, timeout=15)
                            if debug: st.write(f"🐞 Status Fallback: {resp.status_code}")
                        
                        if resp.status_code == 200:
                            img = Image.open(BytesIO(resp.content))
                            set_image(img, f"Pollinations: {query[:20]}...")
                            # Use image object instead of URL to avoid CORS/ORB
                            st.image(img, caption=f"Pollinations AI")
                            st.success("Imagem gerada e carregada no workspace!")
                        else:
                            st.error(f"Erro Pollinations ({resp.status_code}): {resp.text}")
                            
                    except Exception as e:
                         st.error(f"Erro Pollinations: {e}")
                         if debug: st.exception(e)

                elif selected_source == "picsum": # Picsum
                    time.sleep(1.0)
                    base_seed = hash(query)
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        url_a = f"https://picsum.photos/seed/{base_seed}_A/500/300"
                        st.image(url_a, caption="Opção A")
                        if st.button("Selecionar A"):
                            resp = requests.get(url_a)
                            img = Image.open(BytesIO(resp.content))
                            set_image(img, "Opção A")
                    
                    with col2:
                        url_b = f"https://picsum.photos/seed/{base_seed}_B/500/300"
                        st.image(url_b, caption="Opção B")
                        if st.button("Selecionar B"):
                            resp = requests.get(url_b)
                            img = Image.open(BytesIO(resp.content))
                            set_image(img, "Opção B")
                            
                    with col3:
                        url_c = f"https://picsum.photos/seed/{base_seed}_C/500/300"
                        st.image(url_c, caption="Opção C")
                        if st.button("Selecionar C"):
                            resp = requests.get(url_c)
                            img = Image.open(BytesIO(resp.content))
                            set_image(img, "Opção C")

elif mode == "Ateliê de Edição":
    st.subheader("🎨 Ateliê de Manipulação")
    
    uploaded_file = st.file_uploader("Carregue uma imagem manual (opcional)", type=["jpg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        set_image(img, "Upload Manual")

    current_img = st.session_state['workspace']['image_raw']
    
    if current_img:
        col_orig, col_proc = st.columns(2)
        
        with col_orig:
            st.markdown("### Original")
            st.image(current_img, use_column_width=True)
            
            if st.button("🪄 Remover Fundo (Rembg)", type="primary"):
                with st.spinner("O Agente está recortando a realidade pixel a pixel..."):
                    remove = get_rembg() # Importa só agora
                    buf = BytesIO()
                    current_img.save(buf, format="PNG")
                    byte_img = buf.getvalue()
                    result_bytes = remove(byte_img)
                    result_img = Image.open(BytesIO(result_bytes))
                    st.session_state['workspace']['image_processed'] = result_img
                    st.success("Fundo removido!")
        
        with col_proc:
            st.markdown("### Processada")
            if st.session_state['workspace']['image_processed']:
                st.image(st.session_state['workspace']['image_processed'], use_column_width=True)
                buf = BytesIO()
                st.session_state['workspace']['image_processed'].save(buf, format="PNG")
                st.download_button("Baixar PNG", data=buf.getvalue(), file_name="recorte_onirico.png", mime="image/png")
            else:
                st.info("Aguardando processamento...")
                
    else:
        st.warning("Nenhuma imagem no ateliê.")

elif mode == "Montagem de Cena":
    st.subheader("🎞️ Linha do Tempo")
    
    final_img = None
    if st.session_state['workspace']['image_processed']:
        final_img = st.session_state['workspace']['image_processed']
        st.image(final_img, width=200, caption="Usando Imagem Processada")
    elif st.session_state['workspace']['image_raw']:
        final_img = st.session_state['workspace']['image_raw']
        st.image(final_img, width=200, caption="Usando Imagem Original")
    else:
        st.warning("Selecione uma imagem na aba 'Exploração Visual' primeiro.")
        st.stop()
        
    st.write("Conecte as imagens selecionadas com narração e movimento.")
    
    col_script, col_ai = st.columns([3, 1])
    with col_script:
        script = st.text_area("Roteiro da Cena / Legenda", st.session_state.get('last_script', "Volta às aulas com estilo e conforto! #Uniformes2026"))
    with col_ai:
        st.write("🤖 Assistente")
        ai_provider = st.selectbox("IA", ["Gemini", "OpenRouter"], label_visibility="collapsed")
        
        selected_model = "openai/gpt-3.5-turbo" # Default
        if ai_provider == "OpenRouter":
            selected_model = st.selectbox(
                "Modelo OpenRouter", 
                [
                    "google/gemini-2.0-flash-lite-preview-02-05:free",
                    "google/gemini-2.0-pro-exp-02-05:free",
                    "meta-llama/llama-3-8b-instruct:free",
                    "openai/gpt-3.5-turbo",
                    "anthropic/claude-3-haiku"
                ],
                index=0
            )

        if st.button("✨ Magic"):
            with st.spinner(f"{ai_provider} pensando..."):
                topic = st.session_state.get('query_input', "algo inspirador")
                
                if ai_provider == "Gemini":
                    # Fix: use modern model name
                    new_script = generate_script_gemini(topic, model_name="gemini-1.5-flash")
                else:
                    new_script = generate_script_openrouter(topic, model=selected_model)
                    
                st.session_state['last_script'] = new_script
                st.rerun()

    duration = st.slider("Duração (segundos)", 3, 10, 5)
    
    use_elevenlabs = st.toggle("🗣️ Narrar com ElevenLabs")
    
    if st.button("🎬 Renderizar Vídeo Real"):
        available, _, _, _, _ = get_moviepy()
        if available:
            with st.spinner("Renderizando vídeo com MoviePy..."):
                if final_img.mode == 'RGBA':
                    background = Image.new("RGB", final_img.size, (255, 255, 255))
                    background.paste(final_img, mask=final_img.split()[3])
                    video_img = background
                else:
                    video_img = final_img
                
                audio_path = None
                if use_elevenlabs:
                    with st.spinner("Sintetizando voz com ElevenLabs..."):
                        audio_path, error = generate_audio_elevenlabs(script)
                        if error:
                            st.error(error)
                        else:
                            st.success("Áudio gerado!")
                
                video_path = create_video_from_image(video_img, script, duration, audio_path)
                if video_path:
                    st.video(video_path)
                    st.success("Vídeo gerado com sucesso!")
                    with open(video_path, "rb") as v:
                        st.download_button("Baixar MP4", v, file_name="cena_final.mp4", mime="video/mp4")
                    
                    # Limpeza
                    if audio_path:
                        try:
                            os.remove(audio_path)
                        except:
                            pass
                else:
                    st.error("Erro na renderização.")
        else:
            st.error("Biblioteca de vídeo indisponível.")

st.markdown("---")
st.caption("Videos Programáticos - Agente de Co-Criação v1.3 (Lazy Loading)")

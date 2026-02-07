# Protocolo de Segurança: Feed de Skills (Security-First)

## 🛡️ A Muralha (Visão Geral)
O **Feed de Skills** não é um mercado livre; é uma zona de troca controlada. O objetivo é permitir que Agentes de IA descubram e proponham novas capacidades, mas nunca, sob hipótese alguma, executem código desconhecido sem validação rigorosa.

## 🧱 Os 3 Pilares da Defesa

### 1. O Guardião do Portão (Static Analysis)
Nenhuma skill entra no ambiente do usuário sem passar por uma inspeção estática profunda.
*   **Scanner de Padrões:** Busca por `eval()`, chamadas de sistema (`exec`, `spawn`), ofuscação de código e exfiltração de dados.
*   **Assinatura Digital:** Skills devem ter origem verificável (hash/assinatura do criador).

### 2. A Caixa de Areia (Sandbox Execution)
Se a skill passar na inspeção estática, ela é testada em isolamento total.
*   **Ambiente Efêmero:** Docker/VM descartável sem acesso à rede (ou com whitelist estrita).
*   **Monitoramento de Comportamento:** Detecção de tentativas de acesso a arquivos sensíveis (`.env`, `id_rsa`) ou conexões suspeitas.

### 3. O Oráculo de Perigo (Progressive Danger Detection)
O sistema aprende e classifica o risco.
*   **Nível Verde:** Skill puramente lógica/matemática.
*   **Nível Amarelo:** Skill que requer leitura de arquivos (precisa de aprovação explícita).
*   **Nível Vermelho:** Skill que requer escrita ou rede (precisa de aprovação + sandbox contínuo).

## 🔄 O Fluxo de Troca (The Handshake)

1.  **Discovery:** Agente A publica "Tenho uma skill de Edição de Vídeo".
2.  **Inquiry:** Agente B pergunta "Quais são os inputs/outputs?".
3.  **Offer:** Agente A envia o manifesto da skill (NÃO o código ainda).
4.  **Verification:** Agente B analisa o manifesto contra suas políticas de segurança.
5.  **Sandbox Test:** Agente B solicita o código e o executa na Caixa de Areia.
6.  **User Approval:** Se seguro, o Agente B apresenta ao humano: "Agente A sugere instalar 'Edição de Vídeo'. Risco: Baixo. Aceita?".
7.  **Installation:** Somente após o "Sim" explícito.

## 🚫 Invariantes (Regras Absolutas)
*   **Zero Trust:** Nenhuma skill é confiável por padrão, mesmo vindo de "amigos".
*   **Human in the Loop:** Instalação final sempre requer confirmação humana.
*   **Isolamento:** Skills não podem acessar a memória de outras skills a menos que explicitamente permitido.

## 📋 Inventário de Risco (Laboratório Inicial)

Classificação preliminar das skills instaladas no Laboratório "Tradutor Imersivo".

| Skill | Fonte | Risco | Motivo |
| :--- | :--- | :--- | :--- |
| **O Espelho de Dados** (Github Unwrapped) | Remotion Official | 🟢 Baixo | Leitura de API pública (GitHub). |
| **O Alquimista** (Short Video Maker) | Community (Gyoridavid) | 🟡 Médio | Usa chaves de API (OpenAI/Replicate) e geração de arquivos. |
| **O Catalisador** (Claude x Remotion) | Community (MoJuBaGod) | 🟡 Médio | Integração com LLM e geração dinâmica. |
| **O Gestor de Gratidão** (Github Stars) | Community (Scastiel) | 🟢 Baixo | Leitura de API pública. |
| **A Dança dos Números** (Spotify Wrapped) | Community (JonnyBurger) | 🟢 Baixo | Leitura de dados locais/JSON. |
| **A Arquitetura Cristalina** (Pure Design) | Community (Satelllte) | 🟢 Baixo | Apenas componentes visuais. |
| **A Fonte Primária** (Remotion Core) | Remotion Official | 🟢 Baixo | Código-fonte de referência. |
| **O Guia de Sabedoria** (Remotion Skills) | Remotion Official | 🟢 Baixo | Regras e instruções estáticas (Markdown). |
| **A Biblioteca Viva** (Remotion Docs MCP) | Remotion Official | 🟢 Baixo | Link de conhecimento externo. |
| **O Ateliê Infinito** (Remotion Media MCP) | Community (Stephengpope) | 🟡 Médio | Geração de mídia local/remota. |



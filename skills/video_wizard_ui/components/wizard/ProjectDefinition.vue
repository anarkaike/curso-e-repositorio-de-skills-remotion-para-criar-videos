<template>
  <div class="space-y-6">
    
    <!-- 1. Visual Style & Component -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200" :class="{'ring-2 ring-blue-100': sections.visual}">
      <div 
        @click="toggleSection('visual')"
        class="flex items-center justify-between p-6 cursor-pointer bg-white hover:bg-gray-50 transition-colors"
      >
        <div class="flex items-center gap-3">
            <span class="text-2xl bg-blue-50 w-10 h-10 flex items-center justify-center rounded-full">🎨</span>
            <div>
                <h3 class="text-lg font-bold text-gray-900">Estilo Visual</h3>
                <p class="text-sm text-gray-500" v-if="!sections.visual">{{ project.selectedComponent ? availableComponents.find(c => c.id === project.selectedComponent)?.label : 'Selecione um formato' }}</p>
            </div>
        </div>
        <div class="text-gray-400 transition-transform duration-300" :class="{'rotate-180': sections.visual}">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>
      
      <div v-show="sections.visual" class="p-6 pt-0 border-t border-gray-100 bg-gray-50/50">
          <label class="block text-sm font-semibold text-gray-700 mb-2 mt-4">Formato do Conteúdo</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div 
                v-for="comp in availableComponents" 
                :key="comp.id"
                @click="project.selectedComponent = comp.id"
                class="relative flex items-center gap-3 p-3 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md"
                :class="project.selectedComponent === comp.id ? 'border-blue-600 bg-blue-50' : 'border-gray-200 bg-white hover:border-blue-300'"
            >
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-white border border-gray-200 flex items-center justify-center text-lg shadow-sm">
                    {{ getComponentIcon(comp.id) }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-gray-900 truncate">{{ comp.label }}</p>
                </div>
                <div v-if="project.selectedComponent === comp.id" class="absolute top-2 right-2 w-2 h-2 bg-blue-600 rounded-full"></div>
            </div>
          </div>
      </div>
    </div>

    <!-- 2. Core Identity -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200" :class="{'ring-2 ring-purple-100': sections.identity}">
      <div 
        @click="toggleSection('identity')"
        class="flex items-center justify-between p-6 cursor-pointer bg-white hover:bg-gray-50 transition-colors"
      >
        <div class="flex items-center gap-3">
            <span class="text-2xl bg-purple-50 w-10 h-10 flex items-center justify-center rounded-full">🎯</span>
            <div>
                <h3 class="text-lg font-bold text-gray-900">Identidade do Produto</h3>
                <p class="text-sm text-gray-500" v-if="!sections.identity">{{ project.product_name || 'Defina o produto' }}</p>
            </div>
        </div>
        <div class="text-gray-400 transition-transform duration-300" :class="{'rotate-180': sections.identity}">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>

      <div v-show="sections.identity" class="p-6 pt-0 border-t border-gray-100 bg-gray-50/50">
        <div class="space-y-6 mt-4">
            <!-- Product Name -->
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Nome do Produto / Campanha <span class="text-red-500">*</span></label>
                <input v-model="project.product_name" type="text" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 p-3 text-lg font-medium" placeholder="Ex: Coleção Verão 2024" />
                <p class="text-xs text-gray-500 mt-1">Este nome será usado para gerar todas as sugestões abaixo.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Niche -->
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-1">Nicho / Indústria</label>
                    <div class="relative flex rounded-md shadow-sm">
                        <input v-model="project.niche" type="text" placeholder="Ex: Moda, Educação..." class="block w-full rounded-l-lg border-gray-300 focus:border-purple-500 focus:ring-purple-500 p-2.5" />
                        <button @click="getSuggestions('niche')" class="inline-flex items-center px-4 py-2 border border-l-0 border-gray-300 rounded-r-lg bg-white text-sm font-medium text-purple-600 hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors" :disabled="loading.niche">
                            <span v-if="loading.niche" class="animate-spin h-4 w-4 border-2 border-purple-600 border-t-transparent rounded-full"></span>
                            <span v-else>✨ IA</span>
                        </button>
                    </div>
                    <div v-if="suggestions.niche.length > 0" class="mt-2 flex flex-wrap gap-2">
                        <span v-for="sug in suggestions.niche" :key="sug" @click="project.niche = sug" class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-md cursor-pointer hover:bg-purple-100 border border-purple-100 transition-colors">
                            {{ sug }}
                        </span>
                    </div>
                </div>

                <!-- Target Audience -->
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-1">Público Alvo</label>
                    <div class="relative flex rounded-md shadow-sm">
                        <input v-model="project.target_audience" type="text" placeholder="Ex: Jovens Adultos..." class="block w-full rounded-l-lg border-gray-300 focus:border-purple-500 focus:ring-purple-500 p-2.5" />
                        <button @click="getSuggestions('target_audience')" class="inline-flex items-center px-4 py-2 border border-l-0 border-gray-300 rounded-r-lg bg-white text-sm font-medium text-purple-600 hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors" :disabled="loading.target_audience">
                            <span v-if="loading.target_audience" class="animate-spin h-4 w-4 border-2 border-purple-600 border-t-transparent rounded-full"></span>
                            <span v-else>✨ IA</span>
                        </button>
                    </div>
                    <div v-if="suggestions.target_audience.length > 0" class="mt-2 flex flex-wrap gap-2">
                        <span v-for="sug in suggestions.target_audience" :key="sug" @click="project.target_audience = sug" class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-md cursor-pointer hover:bg-purple-100 border border-purple-100 transition-colors">
                            {{ sug }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>

    <!-- 3. Atmosphere & Branding -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200" :class="{'ring-2 ring-indigo-100': sections.atmosphere}">
      <div 
        @click="toggleSection('atmosphere')"
        class="flex items-center justify-between p-6 cursor-pointer bg-white hover:bg-gray-50 transition-colors"
      >
        <div class="flex items-center gap-3">
            <span class="text-2xl bg-indigo-50 w-10 h-10 flex items-center justify-center rounded-full">🌈</span>
            <div>
                <h3 class="text-lg font-bold text-gray-900">Atmosfera & Branding</h3>
                <p class="text-sm text-gray-500" v-if="!sections.atmosphere">{{ project.keywords.length }} tags • {{ project.emotions.length }} emoções</p>
            </div>
        </div>
        <div class="text-gray-400 transition-transform duration-300" :class="{'rotate-180': sections.atmosphere}">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>

      <div v-show="sections.atmosphere" class="p-6 pt-0 border-t border-gray-100 bg-gray-50/50">
        <div class="space-y-6 mt-4">
            <!-- Colors -->
            <div>
                <div class="flex justify-between items-center mb-2">
                     <label class="block text-sm font-semibold text-gray-700">Paleta de Cores</label>
                     <button @click="getSuggestions('colors')" class="text-xs font-medium text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 rounded hover:bg-indigo-50 transition-colors" :disabled="loading.colors">
                         <span v-if="loading.colors" class="animate-spin h-3 w-3 border-2 border-indigo-600 border-t-transparent rounded-full"></span>
                         <span v-else>✨ Sugerir Cores</span>
                     </button>
                </div>
                
                <div class="flex gap-6 items-center bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                    <div class="flex-1">
                        <label class="text-xs text-gray-500 font-medium uppercase tracking-wide mb-1 block">Cor Primária</label>
                        <div class="flex items-center gap-3">
                            <div class="relative h-12 w-12 rounded-full overflow-hidden shadow-inner border border-gray-200 ring-2 ring-offset-1 ring-transparent hover:ring-indigo-200 transition-all">
                                 <input v-model="project.primary_color" type="color" class="absolute -top-4 -left-4 h-20 w-20 cursor-pointer p-0 border-0" />
                            </div>
                            <input v-model="project.primary_color" type="text" class="block w-28 rounded-md border-gray-300 shadow-sm p-2 text-sm uppercase font-mono" maxlength="7" />
                        </div>
                    </div>
                    
                    <div class="text-gray-300">➜</div>

                    <div class="flex-1">
                        <label class="text-xs text-gray-500 font-medium uppercase tracking-wide mb-1 block">Cor Secundária</label>
                        <div class="flex items-center gap-3">
                            <div class="relative h-12 w-12 rounded-full overflow-hidden shadow-inner border border-gray-200 ring-2 ring-offset-1 ring-transparent hover:ring-indigo-200 transition-all">
                                 <input v-model="project.secondary_color" type="color" class="absolute -top-4 -left-4 h-20 w-20 cursor-pointer p-0 border-0" />
                            </div>
                            <input v-model="project.secondary_color" type="text" class="block w-28 rounded-md border-gray-300 shadow-sm p-2 text-sm uppercase font-mono" maxlength="7" />
                        </div>
                    </div>
                </div>

                <!-- Color Suggestions -->
                <div v-if="suggestions.colors.length > 0" class="mt-4">
                    <p class="text-xs text-gray-500 mb-2 font-medium">Sugestões de IA:</p>
                    <div class="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
                        <div v-for="(palette, idx) in suggestions.colors" :key="idx" @click="applyPalette(palette)" class="flex-shrink-0 cursor-pointer border border-gray-200 rounded-lg p-2 hover:bg-indigo-50 hover:border-indigo-300 transition-all group flex flex-col items-center gap-1 min-w-[80px] bg-white shadow-sm" title="Aplicar Paleta">
                            <div class="flex -space-x-3">
                                <div class="w-8 h-8 rounded-full border-2 border-white shadow-sm" :style="{backgroundColor: palette.split(',')[0]}"></div>
                                <div class="w-8 h-8 rounded-full border-2 border-white shadow-sm" :style="{backgroundColor: palette.split(',')[1]}"></div>
                            </div>
                            <span class="text-[10px] text-gray-400 font-mono group-hover:text-indigo-600">Usar</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Keywords -->
            <div>
              <div class="flex justify-between items-center mb-2">
                 <label class="block text-sm font-semibold text-gray-700">Palavras-chave</label>
                 <button @click="getSuggestions('keywords')" class="text-xs font-medium text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 rounded hover:bg-indigo-50 transition-colors" :disabled="loading.keywords">
                     <span v-if="loading.keywords" class="animate-spin h-3 w-3 border-2 border-indigo-600 border-t-transparent rounded-full"></span>
                     <span v-else>✨ Sugerir Tags</span>
                 </button>
              </div>
              <input v-model="keywordsInput" @blur="updateKeywords" type="text" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2.5" placeholder="moderno, limpo, rápido..." />
              
               <div v-if="suggestions.keywords.length > 0" class="mt-3 flex flex-wrap gap-2">
                    <span v-for="kw in suggestions.keywords" :key="kw" @click="addKeyword(kw)" class="text-xs bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-full cursor-pointer hover:bg-indigo-100 border border-indigo-100 flex items-center gap-1 transition-colors font-medium">
                        + {{ kw }}
                    </span>
                </div>
            </div>

            <!-- Emotions -->
            <div>
              <div class="flex justify-between items-center mb-2">
                 <label class="block text-sm font-semibold text-gray-700">Emoções & Tom</label>
                 <button @click="getSuggestions('emotions')" class="text-xs font-medium text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 rounded hover:bg-indigo-50 transition-colors" :disabled="loading.emotions">
                     <span v-if="loading.emotions" class="animate-spin h-3 w-3 border-2 border-indigo-600 border-t-transparent rounded-full"></span>
                     <span v-else>✨ Sugerir Emoções</span>
                 </button>
              </div>
              <div class="flex flex-wrap gap-2">
                <button v-for="emotion in allEmotions" :key="emotion" 
                  @click="toggleEmotion(emotion)"
                  :class="project.emotions.includes(emotion) ? 'bg-indigo-600 text-white shadow-md transform scale-105' : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300'"
                  class="px-4 py-2 rounded-lg text-sm font-medium transition-all border shadow-sm">
                  {{ emotion }}
                </button>
              </div>
            </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
const project = useProject()
const keywordsInput = ref(project.value.keywords.join(', '))

const sections = reactive({
    visual: true,
    identity: true,
    atmosphere: true
})

const toggleSection = (section) => {
    sections[section] = !sections[section]
}

const getComponentIcon = (id) => {
    const icons = {
        'PortraitVideo': '📱',
        'LandscapeVideo': '📺',
        'TopBottomText': '😂',
        'AnimatedTitle': '✨',
        'MotionBlurTitle': '💨',
        'ThreeDScene': '🧊',
        'GifScene': '🎞️',
        'LottiePlayer': '🏃',
        'AnimatedChart': '📊',
        'AudioWaveform': '🔊',
        'NoiseOverlay': '📼',
        'PathDrawing': '🖊️'
    }
    return icons[id] || '📹'
}

const availableComponents = [
  { id: 'PortraitVideo', label: 'Vídeo Vertical (TikTok/Reels)', props: [] },
  { id: 'LandscapeVideo', label: 'Vídeo Horizontal (YouTube)', props: [] },
  { id: 'TopBottomText', label: 'Meme (Texto Topo/Base)', props: [
      { name: 'topText', label: 'Texto Superior', type: 'text' },
      { name: 'bottomText', label: 'Texto Inferior', type: 'text' },
      { name: 'imageSrc', label: 'URL da Imagem', type: 'text' }
  ]},
  { id: 'AnimatedTitle', label: 'Título Animado', props: [
      { name: 'title', label: 'Título Principal', type: 'text' },
      { name: 'subtitle', label: 'Subtítulo', type: 'text' }
  ]},
  { id: 'AnimatedChart', label: 'Gráfico Animado', props: [
      { name: 'data', label: 'Dados (Separados por vírgula)', type: 'array_number' },
      { name: 'labels', label: 'Rótulos (Separados por vírgula)', type: 'array_string' }
  ]},
  { id: 'AudioWaveform', label: 'Onda de Áudio', props: [
      { name: 'audioSrc', label: 'URL do Áudio', type: 'text' }
  ]},
  { id: 'LottiePlayer', label: 'Animação Lottie', props: [
      { name: 'animationUrl', label: 'URL do JSON Lottie', type: 'text' }
  ]},
  { id: 'ThreeDScene', label: 'Cena 3D', props: [
      { name: 'text', label: 'Texto 3D', type: 'text' }
  ]},
  { id: 'MotionBlurTitle', label: 'Título com Motion Blur', props: [
      { name: 'text', label: 'Texto', type: 'text' }
  ]},
  { id: 'GifScene', label: 'Cena com GIF', props: [
      { name: 'gifUrl', label: 'URL do GIF', type: 'text' },
      { name: 'caption', label: 'Legenda', type: 'text' }
  ]},
  { id: 'NoiseOverlay', label: 'Efeito Ruído/Vintage', props: [
      { name: 'text', label: 'Texto', type: 'text' },
      { name: 'noiseOpacity', label: 'Opacidade do Ruído (0.0 - 1.0)', type: 'text' }
  ]},
  { id: 'PathDrawing', label: 'Desenho de Linha (SVG)', props: [
      { name: 'color', label: 'Cor do Traço', type: 'text' }
  ]}
]

const currentComponentProps = computed(() => {
    const comp = availableComponents.find(c => c.id === project.value.selectedComponent)
    return comp ? comp.props : []
})

const suggestions = reactive({
    target_audience: [],
    keywords: [],
    colors: [],
    emotions: [],
    niche: []
})

const loading = reactive({
    target_audience: false,
    keywords: false,
    colors: false,
    emotions: false,
    niche: false
})

const defaultEmotions = ['Feliz', 'Profissional', 'Energético', 'Calmo', 'Confiável', 'Inovador']
const allEmotions = computed(() => [...new Set([...defaultEmotions, ...suggestions.emotions])])

// Sync keywordsInput with project state
watch(() => project.value.keywords, (newVal) => {
    keywordsInput.value = newVal.join(', ')
})

const updateKeywords = () => {
  project.value.keywords = keywordsInput.value.split(',').map(k => k.trim()).filter(k => k)
}

const addKeyword = (kw) => {
    if (!project.value.keywords.includes(kw)) {
        project.value.keywords.push(kw)
    }
}

const toggleEmotion = (emotion) => {
  if (project.value.emotions.includes(emotion)) {
    project.value.emotions = project.value.emotions.filter(e => e !== emotion)
  } else {
    project.value.emotions.push(emotion)
  }
}

const applyPalette = (paletteStr) => {
    if (!paletteStr) return
    const parts = paletteStr.split(',')
    if (parts.length >= 2) {
        project.value.primary_color = parts[0].trim()
        project.value.secondary_color = parts[1].trim()
    }
}

const getSuggestions = async (type, silent = false) => {
    if (loading[type]) return
    
    let context = project.value.product_name
    if (type === 'keywords' && project.value.target_audience) {
        context += ` para ${project.value.target_audience}`
    }
    
    if (!context) {
        if (!silent) alert("Por favor, preencha o nome do produto primeiro.")
        return
    }

    loading[type] = true

    try {
        const result = await $fetch(`http://localhost:35000/suggestions/${type}?context=${encodeURIComponent(context)}`)
        suggestions[type] = result
    } catch (e) {
        console.error(`Error fetching ${type}`, e)
    } finally {
        loading[type] = false
    }
}

// Auto-trigger suggestions when product name changes
let debounceTimer = null
watch(() => project.value.product_name, (newVal) => {
    if (!newVal || newVal.length < 3) return
    
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
        triggerAutoSuggestions()
    }, 1500)
})

const triggerAutoSuggestions = () => {
    const types = ['target_audience', 'niche', 'colors', 'keywords', 'emotions']
    types.forEach(type => {
        if (!loading[type]) {
             getSuggestions(type, true)
        }
    })
}
</script>
<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Product Name -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Nome do Produto</label>
        <div class="flex gap-2">
            <input v-model="project.product_name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" placeholder="Ex: Uniformes Escolares 2024" />
        </div>
        <p class="text-xs text-gray-500 mt-1">O nome principal que aparecerá no vídeo.</p>
      </div>

      <!-- Target Audience with Suggestions -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Público Alvo</label>
        <div class="flex gap-2">
            <input v-model="project.target_audience" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" placeholder="Ex: Diretores de Escola" />
            <button @click="getSuggestions('target_audience')" class="mt-1 px-3 py-2 bg-purple-100 text-purple-700 rounded hover:bg-purple-200 text-sm flex items-center gap-1" :disabled="loading.target_audience">
                <span v-if="loading.target_audience" class="animate-spin h-3 w-3 border-2 border-purple-700 border-t-transparent rounded-full"></span>
                <span v-else>✨ IA</span>
            </button>
        </div>
        <p class="text-xs text-gray-500 mt-1">Quem você quer atingir?</p>
        <!-- Suggestions List -->
        <div v-if="suggestions.target_audience.length > 0" class="mt-2 flex flex-wrap gap-2">
            <span v-for="sug in suggestions.target_audience" :key="sug" @click="project.target_audience = sug" class="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded cursor-pointer hover:bg-purple-100 border border-purple-100">
                {{ sug }}
            </span>
        </div>
      </div>

      <!-- Niche -->
      <div>
         <label class="block text-sm font-medium text-gray-700">Nicho / Indústria</label>
        <input v-model="project.niche" type="text" placeholder="e.g. Têxtil, Escolar" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" />
        <p class="text-xs text-gray-500 mt-1">A área de atuação do seu produto.</p>
      </div>
    </div>

    <!-- Colors with Suggestions -->
    <div>
        <div class="flex justify-between items-center mb-1">
             <label class="block text-sm font-medium text-gray-700">Paleta de Cores</label>
             <button @click="getSuggestions('colors')" class="text-xs text-purple-600 hover:text-purple-800 flex items-center gap-1">
                 ✨ Sugerir Cores
             </button>
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="text-xs text-gray-500">Primária</label>
                <div class="flex gap-2 mt-1">
                    <input v-model="project.primary_color" type="color" class="h-10 w-10 rounded border cursor-pointer" />
                    <input v-model="project.primary_color" type="text" class="block w-full rounded-md border-gray-300 shadow-sm p-2 border text-sm" />
                </div>
            </div>
            <div>
                <label class="text-xs text-gray-500">Secundária</label>
                <div class="flex gap-2 mt-1">
                    <input v-model="project.secondary_color" type="color" class="h-10 w-10 rounded border cursor-pointer" />
                    <input v-model="project.secondary_color" type="text" class="block w-full rounded-md border-gray-300 shadow-sm p-2 border text-sm" />
                </div>
            </div>
        </div>
        <!-- Color Suggestions -->
        <div v-if="suggestions.colors.length > 0" class="mt-2 flex gap-2 overflow-x-auto pb-2">
            <div v-for="(palette, idx) in suggestions.colors" :key="idx" @click="applyPalette(palette)" class="flex-shrink-0 cursor-pointer border rounded p-1 hover:bg-gray-50 flex gap-1 items-center" title="Aplicar Paleta">
                <div class="w-4 h-4 rounded-full border" :style="{backgroundColor: palette.split(',')[0]}"></div>
                <div class="w-4 h-4 rounded-full border" :style="{backgroundColor: palette.split(',')[1]}"></div>
            </div>
        </div>
    </div>

    <!-- Keywords -->
    <div>
      <div class="flex justify-between items-center mb-1">
         <label class="block text-sm font-medium text-gray-700">Palavras-chave</label>
         <button @click="getSuggestions('keywords')" class="text-xs text-purple-600 hover:text-purple-800 flex items-center gap-1">
             ✨ Sugerir Keywords
         </button>
      </div>
      <input v-model="keywordsInput" @blur="updateKeywords" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" placeholder="moderno, limpo, rápido..." />
      <p class="text-xs text-gray-500 mt-1">Termos que descrevem o visual. Separados por vírgula.</p>
       <div v-if="suggestions.keywords.length > 0" class="mt-2 flex flex-wrap gap-2">
            <span v-for="kw in suggestions.keywords" :key="kw" @click="addKeyword(kw)" class="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded cursor-pointer hover:bg-purple-100 border border-purple-100 flex items-center gap-1">
                + {{ kw }}
            </span>
        </div>
    </div>

    <!-- Emotions -->
    <div>
      <div class="flex justify-between items-center mb-1">
         <label class="block text-sm font-medium text-gray-700">Emoções</label>
         <button @click="getSuggestions('emotions')" class="text-xs text-purple-600 hover:text-purple-800 flex items-center gap-1">
             ✨ Sugerir Emoções
         </button>
      </div>
      <div class="flex flex-wrap gap-2 mt-2">
        <button v-for="emotion in allEmotions" :key="emotion" 
          @click="toggleEmotion(emotion)"
          :class="project.emotions.includes(emotion) ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          class="px-3 py-1 rounded-full text-sm font-medium transition-colors border border-transparent">
          {{ emotion }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const project = useProject()
const keywordsInput = ref(project.value.keywords.join(', '))

const suggestions = reactive({
    target_audience: [],
    keywords: [],
    colors: [],
    emotions: []
})

const loading = reactive({
    target_audience: false,
    keywords: false,
    colors: false,
    emotions: false
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
    const [primary, secondary] = paletteStr.split(',')
    project.value.primary_color = primary
    project.value.secondary_color = secondary
}

const getSuggestions = async (type) => {
    if (loading[type]) return
    loading[type] = true
    
    // Construct context based on available info
    let context = project.value.product_name
    if (type === 'keywords' && project.value.target_audience) {
        context += ` para ${project.value.target_audience}`
    }
    
    if (!context) {
        alert("Por favor, preencha o nome do produto primeiro.")
        loading[type] = false
        return
    }

    try {
        const result = await $fetch(`http://localhost:35000/suggestions/${type}?context=${encodeURIComponent(context)}`)
        suggestions[type] = result
    } catch (e) {
        console.error(`Error fetching ${type}`, e)
    } finally {
        loading[type] = false
    }
}
</script>

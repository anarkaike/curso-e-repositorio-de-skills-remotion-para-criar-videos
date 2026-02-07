<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-2 mb-2 border-b border-gray-100 pb-4">
      <span class="text-2xl">🎭</span>
      <div>
        <h3 class="text-lg font-bold text-gray-900">Preferências de Estilo</h3>
        <p class="text-sm text-gray-500">Avalie estes estilos para nos ajudar a definir o visual do vídeo.</p>
      </div>
    </div>

    <!-- Styles Section -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div 
          @click="toggleSection('styles')"
          class="flex items-center justify-between p-6 cursor-pointer bg-white hover:bg-gray-50 transition-colors"
        >
            <div class="flex items-center gap-3">
                <span class="p-2 bg-pink-100 text-pink-600 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
                    </svg>
                </span>
                <div>
                    <h3 class="text-lg font-bold text-gray-900">Sugestões de Estilo</h3>
                    <p class="text-sm text-gray-500" v-if="!sections.styles">
                        {{ loading ? 'Gerando estilos...' : (references.length + ' opções geradas') }}
                    </p>
                </div>
            </div>
            <div class="text-gray-400 transition-transform duration-300" :class="{'rotate-180': sections.styles}">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
            </div>
        </div>

        <div v-show="sections.styles" class="p-6 border-t border-gray-100 bg-gray-50/50 transition-all duration-300 ease-in-out">
            <div v-if="loading" class="flex flex-col items-center justify-center py-20">
                <div class="relative w-20 h-20 mx-auto mb-4">
                    <div class="absolute inset-0 border-4 border-pink-100 rounded-full animate-pulse"></div>
                    <div class="absolute inset-2 border-4 border-pink-500 border-t-transparent rounded-full animate-spin"></div>
                    <div class="absolute inset-0 flex items-center justify-center text-2xl">🎨</div>
                </div>
                <h3 class="text-lg font-medium text-gray-800">{{ loadingStep }}</h3>
                <p class="text-sm text-gray-500 mt-2">Nossos agentes estão trabalhando no seu conceito...</p>
                
                <div class="mt-6 flex justify-center gap-2 text-xs text-gray-400">
                    <span :class="{'text-pink-600 font-bold': loadingStep.includes('Criativo')}">1. Ideação</span> →
                    <span :class="{'text-pink-600 font-bold': loadingStep.includes('Arte')}">2. Geração Visual</span> →
                    <span :class="{'text-pink-600 font-bold': loadingStep.includes('Curador')}">3. Análise</span>
                </div>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div v-for="(ref, index) in references" :key="index" 
                class="group bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col overflow-hidden transform hover:-translate-y-1">
                
                <!-- Image Container -->
                <div class="aspect-video bg-gray-100 relative overflow-hidden">
                    <img :src="ref.url" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" @error="ref.url = 'https://placehold.co/600x400?text=Style+Preview+Error'" />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div class="absolute top-2 right-2 bg-black/60 text-white text-[10px] px-2 py-1 rounded backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity">
                        {{ ref.source }}
                    </div>
                </div>
                
                <div class="p-5 flex flex-col flex-grow">
                    <h3 class="font-bold text-lg text-gray-900 mb-1">{{ ref.style_name }}</h3>
                    <p class="text-sm text-gray-500 mb-6 leading-relaxed line-clamp-3">{{ ref.description }}</p>
                    
                    <div class="mt-auto grid grid-cols-3 gap-2">
                        <button @click="rate(index, 'love')" 
                            :class="[
                                'flex flex-col items-center justify-center py-3 rounded-lg border transition-all duration-200',
                                ref.rating === 'love' 
                                    ? 'bg-green-50 border-green-500 text-green-700 shadow-inner scale-95' 
                                    : 'bg-white border-gray-200 hover:bg-green-50 hover:border-green-300 text-gray-600'
                            ]">
                            <span class="text-xl mb-1 transform transition-transform" :class="ref.rating === 'love' ? 'scale-125' : ''">❤️</span>
                            <span class="text-xs font-semibold">Amei</span>
                        </button>

                        <button @click="rate(index, 'meh')" 
                            :class="[
                                'flex flex-col items-center justify-center py-3 rounded-lg border transition-all duration-200',
                                ref.rating === 'meh' 
                                    ? 'bg-yellow-50 border-yellow-500 text-yellow-700 shadow-inner scale-95' 
                                    : 'bg-white border-gray-200 hover:bg-yellow-50 hover:border-yellow-300 text-gray-600'
                            ]">
                            <span class="text-xl mb-1 transform transition-transform" :class="ref.rating === 'meh' ? 'scale-125' : ''">😐</span>
                            <span class="text-xs font-semibold">Médio</span>
                        </button>

                        <button @click="rate(index, 'hate')" 
                            :class="[
                                'flex flex-col items-center justify-center py-3 rounded-lg border transition-all duration-200',
                                ref.rating === 'hate' 
                                    ? 'bg-red-50 border-red-500 text-red-700 shadow-inner scale-95' 
                                    : 'bg-white border-gray-200 hover:bg-red-50 hover:border-red-300 text-gray-600'
                            ]">
                            <span class="text-xl mb-1 transform transition-transform" :class="ref.rating === 'hate' ? 'scale-125' : ''">👎</span>
                            <span class="text-xs font-semibold">Odiei</span>
                        </button>
                    </div>
                </div>
              </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
const project = useProject()
const loading = ref(true)
const loadingStep = ref('🤖 Agente Criativo: Analisando seu nicho...')
const references = ref([])

const sections = reactive({
    styles: true
})

const toggleSection = (section) => {
    sections[section] = !sections[section]
}

onMounted(async () => {
    // Check if we already have references
    if (project.value.references && project.value.references.length > 0) {
        references.value = project.value.references.map(r => ({
            style_name: r.id,
            description: r.comment,
            url: r.url,
            rating: r.rating,
            source: 'Saved'
        }))
        loading.value = false
        return
    }

    // Start Agent Simulation
    const progressInterval = setInterval(() => {
         if (loadingStep.value.includes('Criativo')) loadingStep.value = '🎨 Agente de Arte: Criando conceitos visuais...'
         else if (loadingStep.value.includes('Arte')) loadingStep.value = '👁️ Agente Curador: Analisando e descrevendo estilos...'
    }, 2000)

    try {
        const niche = project.value.niche || 'Business'
        const theme = project.value.theme || 'Professional'
        
        // Call Agentic Endpoint (simulated or real)
        // Using existing logic but improved
        const keywords = project.value.keywords.join(' ') || 'uniforms'
        const styles = [
            { name: 'Minimalista e Limpo', prompt: `minimalist clean design ${keywords}, high key lighting, white background` },
            { name: 'Ousado e Energético', prompt: `bold colorful energetic ${keywords}, dynamic angles, vibrant colors` },
            { name: 'Corporativo Profissional', prompt: `corporate professional trusted ${keywords}, blue tones, office setting` }
        ]

        // Simulate network delay for agent effect
        await new Promise(resolve => setTimeout(resolve, 6000))

        references.value = styles.map(s => {
            const originalUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(s.prompt)}?nologo=true&seed=${Math.floor(Math.random() * 1000)}`
            return {
                style_name: s.name,
                description: s.prompt,
                url: `http://localhost:35000/proxy/image?url=${encodeURIComponent(originalUrl)}`,
                rating: null,
                source: 'AI Agent'
            }
        })
    } catch (e) {
        console.error("Agent Error", e)
    } finally {
        clearInterval(progressInterval)
        loading.value = false
    }
})

const rate = (index, rating) => {
    references.value[index].rating = rating
    // Update project state immediately
    updateProjectReferences()
}

const updateProjectReferences = () => {
    project.value.references = references.value.map(r => ({
      id: r.style_name,
      url: r.url,
      type: 'image',
      rating: r.rating,
      comment: r.description
    }))
}
</script>

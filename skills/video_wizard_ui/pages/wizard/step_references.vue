<template>
  <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
        <div>
            <h2 class="text-xl font-semibold">Passo 3: Preferências de Estilo</h2>
            <p class="text-gray-600">Estilos curados por Agentes de IA baseados no seu perfil ({{ project.niche }} / {{ project.theme }}).</p>
        </div>
        <button @click="loadStyles" class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
            Consultar Agentes Novamente
        </button>
    </div>

    <div v-if="loading" class="text-center py-16 bg-gray-50 rounded-lg border border-dashed border-gray-200">
        <div class="relative w-20 h-20 mx-auto mb-4">
            <div class="absolute inset-0 border-4 border-blue-100 rounded-full animate-pulse"></div>
            <div class="absolute inset-2 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center text-2xl">🤖</div>
        </div>
        <h3 class="text-lg font-medium text-gray-800">{{ currentStep }}</h3>
        <p class="text-sm text-gray-500 mt-2">Nossos agentes estão trabalhando no seu conceito...</p>
        
        <div class="mt-6 flex justify-center gap-2 text-xs text-gray-400">
            <span :class="{'text-blue-600 font-bold': currentStep.includes('Criativo')}">1. Ideação</span> →
            <span :class="{'text-blue-600 font-bold': currentStep.includes('Arte')}">2. Geração Visual</span> →
            <span :class="{'text-blue-600 font-bold': currentStep.includes('Curador')}">3. Análise & Curadoria</span>
        </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="(ref, index) in references" :key="index" class="border rounded-lg p-4 flex flex-col hover:shadow-md transition-shadow bg-white">
        <div class="aspect-video bg-gray-100 rounded-md mb-4 overflow-hidden relative group">
            <img :src="ref.url" class="w-full h-full object-cover" @error="ref.url = 'https://placehold.co/600x400?text=Style+Preview+Error'" />
            <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all"></div>
            <div class="absolute top-2 right-2 bg-black bg-opacity-60 text-white text-[10px] px-2 py-1 rounded backdrop-blur-sm border border-white/20">
                {{ ref.source }}
            </div>
        </div>
        <h3 class="font-medium text-lg mb-1 text-gray-800">{{ ref.style_name }}</h3>
        <p class="text-xs text-gray-500 mb-4 min-h-[40px]">{{ ref.description }}</p>
        
        <div class="mt-auto">
            <div class="flex justify-between gap-2 mb-3">
                <button @click="rate(index, 'love')" 
                    :class="ref.rating === 'love' ? 'bg-green-100 border-green-500 text-green-700 ring-2 ring-green-200' : 'bg-white border-gray-200 hover:bg-gray-50'"
                    class="flex-1 py-2 border rounded-md text-sm font-medium transition-all transform active:scale-95 flex items-center justify-center gap-1">
                    ❤️ Amei
                </button>
                <button @click="rate(index, 'meh')" 
                    :class="ref.rating === 'meh' ? 'bg-yellow-100 border-yellow-500 text-yellow-700 ring-2 ring-yellow-200' : 'bg-white border-gray-200 hover:bg-gray-50'"
                    class="flex-1 py-2 border rounded-md text-sm font-medium transition-all transform active:scale-95 flex items-center justify-center gap-1">
                    😐 Médio
                </button>
                <button @click="rate(index, 'hate')" 
                    :class="ref.rating === 'hate' ? 'bg-red-100 border-red-500 text-red-700 ring-2 ring-red-200' : 'bg-white border-gray-200 hover:bg-gray-50'"
                    class="flex-1 py-2 border rounded-md text-sm font-medium transition-all transform active:scale-95 flex items-center justify-center gap-1">
                    👎 Odiei
                </button>
            </div>
            
            <!-- Optional Feedback -->
            <div v-if="ref.rating" class="animate-fade-in">
                <input type="text" v-model="ref.feedback" placeholder="O que você gostou/não gostou?" class="w-full text-xs border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" />
            </div>
        </div>
      </div>
    </div>

    <div class="flex justify-between mt-8">
      <button @click="router.back()" class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">Voltar</button>
      <button @click="saveAndNext" class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Próximo: Selecionar Conteúdo</button>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const project = useProject()
const loading = ref(true)
const references = ref([])
const currentStep = ref('')

onMounted(async () => {
    loadStyles()
})

const loadStyles = async () => {
    loading.value = true
    currentStep.value = '🤖 Agente Criativo: Analisando seu nicho...'
    
    const progressInterval = setInterval(() => {
         if (currentStep.value.includes('Criativo')) currentStep.value = '🎨 Agente de Arte: Criando conceitos visuais...'
         else if (currentStep.value.includes('Arte')) currentStep.value = '👁️ Agente Curador: Analisando e descrevendo estilos...'
    }, 2500)

    try {
        const niche = project.value.niche || 'Business'
        const theme = project.value.theme || 'Professional'
        
        // Call our Agentic Endpoint
        const data = await $fetch(`http://localhost:35000/agents/styles?niche=${encodeURIComponent(niche)}&theme=${encodeURIComponent(theme)}`)
        
        references.value = data.map(item => {
            // Ensure we have a valid prompt
            const prompt = item.prompt || `${item.style_name} ${niche} ${theme}`
            const seed = Math.floor(Math.random() * 10000)
            const originalUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?nologo=true&seed=${seed}`
            
            return {
                style_name: item.style_name,
                description: item.description,
                url: `http://localhost:35000/proxy/image?url=${encodeURIComponent(originalUrl)}`,
                rating: null,
                feedback: '',
                source: 'Agent AI'
            }
        })
    } catch (e) {
        console.error('Agent Pipeline Failed:', e)
        // Fallback to static styles if agents fail
        const keywords = project.value.keywords.join(' ') || 'uniforms'
        references.value = [
            { name: 'Minimalista (Fallback)', prompt: `minimalist clean design ${keywords}` },
            { name: 'Ousado (Fallback)', prompt: `bold colorful energetic ${keywords}` },
            { name: 'Corporativo (Fallback)', prompt: `corporate professional trusted ${keywords}` }
        ].map(s => ({
            style_name: s.name,
            description: s.prompt,
            url: `http://localhost:35000/proxy/image?url=${encodeURIComponent(`https://image.pollinations.ai/prompt/${encodeURIComponent(s.prompt)}`)}`,
            rating: null,
            feedback: '',
            source: 'System Backup'
        }))
    } finally {
        clearInterval(progressInterval)
        loading.value = false
    }
}

const rate = (index, rating) => {
    references.value[index].rating = rating
}

const saveAndNext = async () => {
  // Save ratings to project
  project.value.references = references.value.map(r => ({
      id: r.style_name,
      url: r.url,
      type: 'image',
      rating: r.rating,
      comment: r.feedback || r.description 
  }))

  try {
    await $fetch(`http://localhost:35000/projects/${project.value.id}`, {
        method: 'PUT',
        body: project.value
    })
    router.push('/wizard/step2')
  } catch (e) {
      console.error(e)
      alert('Failed to save preferences')
  }
}
</script>

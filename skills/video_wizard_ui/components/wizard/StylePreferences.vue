<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-center gap-2 mb-4 border-b border-gray-100 pb-4">
      <span class="text-2xl">🎭</span>
      <div>
        <h3 class="text-lg font-bold text-gray-900">Preferências de Estilo</h3>
        <p class="text-sm text-gray-500">Avalie estes estilos para nos ajudar a definir o visual do vídeo.</p>
      </div>
    </div>

    <div v-if="loading" class="flex flex-col items-center justify-center py-20 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
        <div class="relative">
            <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
            <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xl">🎨</span>
            </div>
        </div>
        <p class="mt-6 text-gray-600 font-medium">Gerando referências de estilo com IA...</p>
        <p class="text-sm text-gray-400 mt-2">Isso pode levar alguns segundos</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div v-for="(ref, index) in references" :key="index" 
        class="group bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col overflow-hidden transform hover:-translate-y-1">
        
        <!-- Image Container -->
        <div class="aspect-video bg-gray-100 relative overflow-hidden">
            <img :src="ref.url" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" @error="ref.url = 'https://placehold.co/600x400?text=Style+Preview+Error'" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        </div>
        
        <div class="p-5 flex flex-col flex-grow">
            <h3 class="font-bold text-lg text-gray-900 mb-1">{{ ref.style_name }}</h3>
            <p class="text-sm text-gray-500 mb-6 leading-relaxed">{{ ref.description }}</p>
            
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
</template>

<script setup>
const project = useProject()
const loading = ref(true)
const references = ref([])

onMounted(async () => {
    // Generate reference images based on project keywords
    const keywords = project.value.keywords.join(' ') || 'uniforms'
    const styles = [
        { name: 'Minimalista e Limpo', prompt: `minimalist clean design ${keywords}, high key lighting, white background` },
        { name: 'Ousado e Energético', prompt: `bold colorful energetic ${keywords}, dynamic angles, vibrant colors` },
        { name: 'Corporativo Profissional', prompt: `corporate professional trusted ${keywords}, blue tones, office setting` }
    ]

    // Check if we already have references
    if (project.value.references && project.value.references.length > 0) {
        references.value = project.value.references.map(r => ({
            style_name: r.id,
            description: r.comment,
            url: r.url,
            rating: r.rating
        }))
        loading.value = false
        return
    }

    // Simulate fetching/generating
    references.value = styles.map(s => {
        const originalUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(s.prompt)}?nologo=true&seed=${Math.floor(Math.random() * 1000)}`
        return {
            style_name: s.name,
            description: s.prompt,
            url: `http://localhost:35000/proxy/image?url=${encodeURIComponent(originalUrl)}`,
            rating: null
        }
    })
    
    // Fake loading delay for UX
    setTimeout(() => { loading.value = false }, 1000)
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

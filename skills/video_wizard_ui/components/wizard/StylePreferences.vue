<template>
  <div class="space-y-6">
    <p class="text-gray-600 mb-6">Avalie estes estilos para nos ajudar a definir o visual do vídeo.</p>

    <div v-if="loading" class="text-center py-10">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-500">Gerando referências de estilo...</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="(ref, index) in references" :key="index" class="border rounded-lg p-4 flex flex-col">
        <div class="aspect-video bg-gray-100 rounded-md mb-4 overflow-hidden">
            <img :src="ref.url" class="w-full h-full object-cover" @error="ref.url = 'https://placehold.co/600x400?text=Style+Preview+Error'" />
        </div>
        <h3 class="font-medium text-lg mb-2">{{ ref.style_name }}</h3>
        <p class="text-sm text-gray-500 mb-4">{{ ref.description }}</p>
        
        <div class="mt-auto flex justify-between gap-2">
            <button @click="rate(index, 'love')" 
                :class="ref.rating === 'love' ? 'bg-green-100 border-green-500 text-green-700' : 'bg-white border-gray-200 hover:bg-gray-50'"
                class="flex-1 py-2 border rounded-md text-sm font-medium transition-colors">
                ❤️ Amei
            </button>
            <button @click="rate(index, 'meh')" 
                :class="ref.rating === 'meh' ? 'bg-yellow-100 border-yellow-500 text-yellow-700' : 'bg-white border-gray-200 hover:bg-gray-50'"
                class="flex-1 py-2 border rounded-md text-sm font-medium transition-colors">
                😐 Médio
            </button>
            <button @click="rate(index, 'hate')" 
                :class="ref.rating === 'hate' ? 'bg-red-100 border-red-500 text-red-700' : 'bg-white border-gray-200 hover:bg-gray-50'"
                class="flex-1 py-2 border rounded-md text-sm font-medium transition-colors">
                👎 Odiei
            </button>
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

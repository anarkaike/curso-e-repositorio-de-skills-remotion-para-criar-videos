<template>
  <div class="space-y-6">
    <div class="mb-6 border-b pb-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Marca & Template</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
              <label class="block text-sm font-medium text-gray-700">Template de Vídeo</label>
              <select v-model="template" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                  <option value="simple">Simples e Limpo</option>
                  <option value="corporate">Barra Corporativa</option>
                  <option value="bold">Moldura Ousada</option>
              </select>
              <p class="text-xs text-gray-500 mt-1">O estilo visual da montagem do vídeo.</p>
          </div>
          <div>
              <label class="block text-sm font-medium text-gray-700">Texto do Cabeçalho</label>
              <input type="text" v-model="headerText" placeholder="e.g. Nova Coleção" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
              <p class="text-xs text-gray-500 mt-1">Texto curto no topo do vídeo.</p>
          </div>
          <div>
              <label class="block text-sm font-medium text-gray-700">Texto do Rodapé</label>
              <input type="text" v-model="footerText" placeholder="e.g. www.seusite.com.br" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
              <p class="text-xs text-gray-500 mt-1">Texto no rodapé, ideal para site ou telefone.</p>
          </div>
      </div>
    </div>

    <div class="mb-6">
      <div class="flex justify-between items-center mb-2">
          <h3 class="text-lg font-medium text-gray-900">Sugestões de IA & Busca Web</h3>
          <button @click="loadSuggestions" class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
              Regerar Ideias
          </button>
      </div>
      <div v-if="loading" class="text-center py-10">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-2 text-gray-500">Caçando visuais...</p>
      </div>
      <div v-else class="grid grid-cols-3 gap-4">
        <div 
          v-for="img in suggestions" 
          :key="img.url" 
          class="relative group cursor-pointer border rounded-lg overflow-hidden transition-all duration-200 aspect-[9/16]"
          :class="{'ring-4 ring-blue-500 transform scale-105': selectedImages.has(img.url)}"
          @click="toggleImage(img.url)"
        >
          <img :src="img.url" :alt="img.description" class="w-full h-full object-cover" @error="img.url = 'https://placehold.co/600x400?text=Image+Error'" />
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center">
             <div v-if="selectedImages.has(img.url)" class="absolute top-2 right-2 bg-blue-600 text-white rounded-full p-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
             </div>
             <span class="absolute bottom-2 left-2 bg-white px-2 py-1 rounded text-xs opacity-75 truncate max-w-[90%]">{{ img.source }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-6">
       <h3 class="text-lg font-medium text-gray-900 mb-2">Envie os Seus</h3>
       <input type="file" multiple @change="handleFileUpload" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
    </div>

    <div class="flex justify-end mt-6">
        <button 
          @click="finish" 
          :disabled="selectedImages.size === 0 || generating"
          class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <span v-if="generating" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          {{ generating ? 'Gerando...' : `Finalizar & Gerar (${selectedImages.size})` }}
        </button>
      </div>
  </div>
</template>

<script setup>
const project = useProject()
const suggestions = ref([])
const loading = ref(true)
const selectedImages = ref(new Set())
const generating = ref(false)

// Branding State
const template = ref('simple')
const headerText = ref('')
const footerText = ref('')

onMounted(() => {
    // Set defaults
    headerText.value = project.value.product_name || project.value.name || 'Vídeo Showcase'
    footerText.value = 'www.seusite.com.br'
    loadSuggestions()
})

const loadSuggestions = async () => {
    loading.value = true
    try {
        const query = `${project.value.theme} ${project.value.keywords.join(' ')}`
        // Add random param to force refresh if backend caches
        suggestions.value = await $fetch(`http://localhost:35000/suggestions/images?query=${encodeURIComponent(query)}&t=${Date.now()}`)
    } catch (e) {
        console.error("Failed to load suggestions", e)
    } finally {
        loading.value = false
    }
}

const toggleImage = (url) => {
  if (selectedImages.value.has(url)) {
    selectedImages.value.delete(url)
  } else {
    selectedImages.value.add(url)
  }
}

const handleFileUpload = async (event) => {
  const files = Array.from(event.target.files)
  for (const file of files) {
      const formData = new FormData()
      formData.append('file', file)
      try {
          const response = await $fetch('http://localhost:35000/upload/image', {
              method: 'POST',
              body: formData
          })
          if (response.url) {
            suggestions.value.unshift({
                url: response.url,
                source: "Uploaded",
                description: file.name
            })
            selectedImages.value.add(response.url)
          }
      } catch (e) {
          console.error("Upload failed", e)
      }
  }
}

const finish = async () => {
  generating.value = true
  try {
      // Save project first to ensure consistency
      await $fetch(`http://localhost:35000/projects/${project.value.id}`, {
          method: 'PUT',
          body: project.value
      })

      // Construct a simple script based on keywords if not provided
      const script = `Promotional video for ${project.value.product_name || project.value.name}. ` +
                     `Theme: ${project.value.theme}. ` + 
                     `Keywords: ${project.value.keywords.join(', ')}. ` +
                     `Targeting: ${project.value.target_audience}.`

      const result = await $fetch('http://localhost:35000/generate/video', {
          method: 'POST',
          body: {
              project_id: project.value.id,
              selected_images: Array.from(selectedImages.value),
              script_text: script,
              template: template.value,
              header_text: headerText.value,
              footer_text: footerText.value
          }
      })
      
      if (result.status === 'success') {
          alert(`Vídeo Gerado com Sucesso!\nID do Job: ${result.job_id}`)
          window.open(result.video_url, '_blank')
      } else {
          alert("Falha na geração: " + (result.error || 'Erro desconhecido'))
      }
  } catch (e) {
      console.error(e)
      alert("Falha ao iniciar geração: " + e.message)
  } finally {
      generating.value = false
  }
}
</script>

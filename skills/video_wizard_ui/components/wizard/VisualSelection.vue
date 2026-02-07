<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-center gap-2 mb-4 border-b border-gray-100 pb-4">
      <span class="text-2xl">🎬</span>
      <div>
        <h3 class="text-lg font-bold text-gray-900">Finalização & Visual</h3>
        <p class="text-sm text-gray-500">Escolha o template final e selecione as melhores imagens para o seu vídeo.</p>
      </div>
    </div>

    <!-- Template Selection -->
    <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
      <h4 class="text-md font-semibold text-gray-900 mb-4 flex items-center gap-2">
         <span class="p-1 bg-indigo-100 text-indigo-600 rounded">Layout</span>
         Escolha o Template
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <label 
            v-for="opt in templateOptions" 
            :key="opt.value"
            class="relative flex flex-col cursor-pointer border-2 rounded-xl p-4 transition-all hover:border-blue-400"
            :class="template === opt.value ? 'border-blue-600 bg-blue-50' : 'border-gray-200 bg-white'"
          >
              <input type="radio" v-model="template" :value="opt.value" class="sr-only">
              <div class="flex items-center justify-between mb-2">
                  <span class="font-medium text-gray-900">{{ opt.label }}</span>
                  <div v-if="template === opt.value" class="h-5 w-5 rounded-full bg-blue-600 text-white flex items-center justify-center">
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                  </div>
              </div>
              <p class="text-xs text-gray-500">{{ opt.desc }}</p>
          </label>
      </div>
    </div>

    <!-- Text Inputs -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Texto do Cabeçalho</label>
            <input type="text" v-model="headerText" placeholder="e.g. Nova Coleção" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2.5 bg-gray-50 border">
            <p class="text-xs text-gray-500 mt-1">Texto curto no topo do vídeo.</p>
        </div>
        <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Texto do Rodapé</label>
            <input type="text" v-model="footerText" placeholder="e.g. www.seusite.com.br" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2.5 bg-gray-50 border">
            <p class="text-xs text-gray-500 mt-1">Texto no rodapé (site, telefone).</p>
        </div>
    </div>

    <!-- Image Selection -->
    <div>
      <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="text-lg font-bold text-gray-900">Seleção de Mídia</h3>
            <p class="text-sm text-gray-500">Selecione as imagens que aparecerão no vídeo.</p>
          </div>
          <div class="flex gap-2">
            <label class="cursor-pointer px-3 py-1.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                <input type="file" multiple @change="handleFileUpload" class="hidden" />
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                Upload
            </label>
            <button @click="loadSuggestions" class="px-3 py-1.5 border border-blue-200 bg-blue-50 rounded-lg text-sm font-medium text-blue-700 hover:bg-blue-100 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                Regerar IA
            </button>
          </div>
      </div>

      <div v-if="loading" class="text-center py-20 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-500">Caçando visuais perfeitos...</p>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <div 
          v-for="img in suggestions" 
          :key="img.url" 
          class="relative group cursor-pointer rounded-lg overflow-hidden aspect-[9/16] transition-all duration-200"
          :class="selectedImages.has(img.url) ? 'ring-4 ring-blue-500 shadow-lg transform scale-[1.02]' : 'border border-gray-200 hover:shadow-md'"
          @click="toggleImage(img.url)"
        >
          <img :src="img.url" :alt="img.description" class="w-full h-full object-cover" @error="img.url = 'https://placehold.co/600x400?text=Image+Error'" />
          
          <!-- Selection Overlay -->
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all flex items-center justify-center">
             <div v-if="selectedImages.has(img.url)" class="absolute top-2 right-2 bg-blue-600 text-white rounded-full p-1 shadow-sm animate-bounce-short">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
             </div>
             <span class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2 pt-6 text-white text-[10px] truncate">{{ img.source }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Final Action -->
    <div class="flex justify-end pt-6 border-t border-gray-100">
        <button 
          @click="finish" 
          :disabled="generating"
          class="py-3 px-6 rounded-xl shadow-lg text-base font-bold text-white bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3 transition-all transform hover:scale-[1.02]"
        >
          <span v-if="generating" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
          <span v-else class="text-xl">✨</span>
          {{ generating ? 'Gerando Vídeo...' : (selectedImages.size === 0 ? 'Gerar com IA (Automático)' : `Finalizar & Gerar (${selectedImages.size} assets)`) }}
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

const templateOptions = [
    { value: 'simple', label: 'Simples e Limpo', desc: 'Minimalista, foco no conteúdo.' },
    { value: 'corporate', label: 'Barra Corporativa', desc: 'Profissional, com rodapé fixo.' },
    { value: 'bold', label: 'Moldura Ousada', desc: 'Alto impacto, bordas coloridas.' }
]

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
      // Auto-select images if none selected
      if (selectedImages.value.size === 0) {
        if (suggestions.value.length > 0) {
            // Select top 5
            suggestions.value.slice(0, 5).forEach(img => selectedImages.value.add(img.url))
        } else {
            // Fallback if no suggestions loaded yet
            await loadSuggestions()
            if (suggestions.value.length > 0) {
                 suggestions.value.slice(0, 5).forEach(img => selectedImages.value.add(img.url))
            } else {
                // Absolute fallback
                selectedImages.value.add('https://placehold.co/600x400?text=AI+Generated+Content')
            }
        }
      }

      // Save project first to ensure consistency
      // Update context photos with selected images
      project.value.context_photos = Array.from(selectedImages.value)
      
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

<template>
  <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4">Passo 2: Contexto & Arquivos</h2>
    <p class="text-gray-600 mb-6">Envie logotipos e fotos reais para ajudar a IA a entender sua marca.</p>

    <div class="space-y-6">
      <!-- Logo Upload -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Logotipo (PNG Transparente)</label>
        <div class="flex items-center gap-4">
          <input type="file" accept="image/png" @change="uploadLogo" class="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100
          "/>
          <img v-if="project.logo_path" :src="project.logo_path" class="h-12 w-12 object-contain border rounded" />
        </div>
        <p class="text-xs text-gray-500 mt-1">Sua marca com fundo transparente para melhor qualidade.</p>
      </div>

      <!-- General Uploads -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Fotos da Empresa (Loja, Equipe, Produtos)</label>
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
            <input type="file" multiple accept="image/*" @change="uploadPhotos" class="hidden" id="photos-upload" />
            <label for="photos-upload" class="cursor-pointer">
                <div class="text-gray-600">
                    <span class="text-blue-600 font-medium">Clique para enviar</span> ou arraste e solte
                </div>
                <p class="text-xs text-gray-500 mt-1">PNG, JPG até 10MB</p>
            </label>
        </div>
        <p class="text-xs text-gray-500 mt-1">Fotos reais do seu negócio para dar autenticidade.</p>
        
        <!-- Preview Grid -->
        <div v-if="uploadedPhotos.length > 0" class="grid grid-cols-4 gap-4 mt-4">
            <div v-for="(photo, index) in uploadedPhotos" :key="index" class="relative group">
                <img :src="photo" class="h-24 w-full object-cover rounded-md" />
                <button @click="removePhoto(index)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>
        </div>
      </div>

      <div class="flex justify-between mt-6">
        <button @click="router.back()" class="py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">Voltar</button>
        <button @click="saveAndNext" class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Próximo: Preferências de Estilo</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const project = useProject()
const uploadedPhotos = ref([]) // Temporary local state for preview

const uploadFile = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    try {
        const response = await $fetch('http://localhost:35000/upload/image', {
            method: 'POST',
            body: formData
        })
        return response.url
    } catch (e) {
        console.error('Upload failed', e)
        alert('Upload failed')
        return null
    }
}

const uploadLogo = async (event) => {
    const file = event.target.files[0]
    if (!file) return
    const url = await uploadFile(file)
    if (url) {
        project.value.logo_path = url
    }
}

const uploadPhotos = async (event) => {
    const files = Array.from(event.target.files)
    for (const file of files) {
        const url = await uploadFile(file)
        if (url) {
            uploadedPhotos.value.push(url)
            // We might want to store these somewhere in the project model too
            // For now let's assume they are part of "selected_images" or similar, 
            // or just context. Let's add them to a 'context_photos' array if we had one.
            // For this MVP, let's just push them to a temporary list in project to save.
            if (!project.value.context_photos) project.value.context_photos = []
            project.value.context_photos.push(url)
        }
    }
}

const removePhoto = (index) => {
    uploadedPhotos.value.splice(index, 1)
    if (project.value.context_photos) {
        project.value.context_photos.splice(index, 1)
    }
}

const saveAndNext = async () => {
  try {
    await $fetch(`http://localhost:35000/projects/${project.value.id}`, {
        method: 'PUT',
        body: project.value
    })
    router.push('/wizard/step_references')
  } catch (e) {
      console.error(e)
      alert('Failed to save context')
  }
}
</script>

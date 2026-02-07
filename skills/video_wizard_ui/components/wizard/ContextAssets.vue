<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-center gap-2 mb-4 border-b border-gray-100 pb-4">
      <span class="text-2xl">🖼️</span>
      <div>
        <h3 class="text-lg font-bold text-gray-900">Ativos Visuais</h3>
        <p class="text-sm text-gray-500">Envie logotipos e fotos reais para ajudar a IA a entender sua marca.</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Logo Upload Section -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center gap-2 mb-4">
            <span class="p-2 bg-blue-100 text-blue-600 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
                </svg>
            </span>
            <label class="block text-base font-semibold text-gray-900">Logotipo</label>
        </div>
        
        <div class="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-blue-500 hover:bg-blue-50 transition-all cursor-pointer relative group">
          <input type="file" accept="image/png" @change="uploadLogo" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
          
          <div v-if="project.logo_path" class="relative z-20">
             <img :src="project.logo_path" class="h-32 w-32 object-contain drop-shadow-sm" />
             <div class="absolute -bottom-2 -right-2 bg-green-500 text-white rounded-full p-1 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
             </div>
          </div>
          <div v-else class="text-center">
             <div class="mx-auto h-12 w-12 text-gray-400 group-hover:text-blue-500 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
             </div>
             <p class="mt-2 text-sm font-medium text-gray-900">Clique para enviar logo</p>
             <p class="mt-1 text-xs text-gray-500">PNG Transparente recomendado</p>
          </div>
        </div>
      </div>

      <!-- Photos Upload Section -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
         <div class="flex items-center gap-2 mb-4">
            <span class="p-2 bg-purple-100 text-purple-600 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
                </svg>
            </span>
            <label class="block text-base font-semibold text-gray-900">Fotos da Empresa</label>
        </div>

        <div class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-purple-500 hover:bg-purple-50 transition-all cursor-pointer relative group h-48 flex flex-col justify-center items-center">
            <input type="file" multiple accept="image/*" @change="uploadPhotos" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
            <div class="mx-auto h-12 w-12 text-gray-400 group-hover:text-purple-500 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
            </div>
            <div class="text-gray-600 mt-2">
                <span class="text-purple-600 font-medium">Clique para enviar</span> ou arraste
            </div>
            <p class="text-xs text-gray-500 mt-1">Loja, equipe, produtos (PNG, JPG)</p>
        </div>
      </div>
    </div>

    <!-- Preview Grid (Full Width) -->
    <div v-if="project.context_photos && project.context_photos.length > 0" class="mt-6">
        <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
            <span>Galeria Enviada</span>
            <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">{{ project.context_photos.length }}</span>
        </h4>
        <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 gap-4">
            <div v-for="(photo, index) in project.context_photos" :key="index" class="relative group aspect-square rounded-lg overflow-hidden border border-gray-200 shadow-sm">
                <img :src="photo" class="w-full h-full object-cover transition-transform group-hover:scale-105" />
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all"></div>
                <button @click="removePhoto(index)" class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1.5 shadow-md opacity-0 group-hover:opacity-100 transition-all transform hover:scale-110">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
const project = useProject()

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
            if (!project.value.context_photos) project.value.context_photos = []
            project.value.context_photos.push(url)
        }
    }
}

const removePhoto = (index) => {
    if (project.value.context_photos) {
        project.value.context_photos.splice(index, 1)
    }
}
</script>

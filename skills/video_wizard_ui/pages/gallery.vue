<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Gallery</h2>
      <button @click="fetchProjects" class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-500">Loading gallery...</p>
    </div>

    <div v-else-if="projects.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">No projects found. Start by creating a new project!</p>
      <NuxtLink to="/" class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Go to Wizard
      </NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="p in projects" :key="p.id" class="bg-white rounded-lg shadow-md overflow-hidden flex flex-col">
        <!-- Video Preview or Placeholder -->
        <div class="aspect-video bg-gray-100 relative group">
          <video 
            v-if="p.output_video_url" 
            controls 
            class="w-full h-full object-cover"
            :poster="p.output_video_url ? '' : 'https://placehold.co/600x400?text=No+Video'"
          >
            <source :src="p.output_video_url" type="video/mp4">
            Your browser does not support the video tag.
          </video>
          <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <span class="text-sm">Not generated yet</span>
          </div>
          
          <!-- Overlay actions -->
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
            <NuxtLink :to="{ path: '/wizard/step1', query: { projectId: p.id } }" class="bg-white text-blue-600 px-4 py-2 rounded-full font-medium shadow-lg hover:bg-blue-50 transform hover:scale-105 transition-all" @click="loadProject(p)">
              {{ p.output_video_url ? 'Edit / Regenerate' : 'Open in Wizard' }}
            </NuxtLink>
          </div>
        </div>

        <div class="p-4 flex-1 flex flex-col">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-bold text-lg truncate" :title="p.name">{{ p.name }}</h3>
            <span class="text-xs px-2 py-1 bg-gray-200 rounded-full shrink-0 ml-2">{{ p.selected_component }}</span>
          </div>
          
          <div class="space-y-1 text-sm text-gray-600 flex-1">
            <p><span class="font-medium">Theme:</span> {{ p.theme }}</p>
            <p v-if="p.product_name"><span class="font-medium">Product:</span> {{ p.product_name }}</p>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center text-xs text-gray-500">
            <span>ID: {{ p.id.substring(0, 8) }}...</span>
            <span v-if="p.output_video_url" class="text-green-600 font-medium flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              Ready
            </span>
            <span v-else class="text-amber-600 font-medium flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              Draft
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const projects = ref([])
const loading = ref(true)
const projectStore = useProject()
const router = useRouter()

const fetchProjects = async () => {
  loading.value = true
  try {
    const data = await $fetch('http://localhost:35000/projects')
    // Sort: projects with video first, then by name
    projects.value = data.sort((a, b) => {
      if (a.output_video_url && !b.output_video_url) return -1
      if (!a.output_video_url && b.output_video_url) return 1
      return 0
    })
  } catch (e) {
    console.error('Failed to fetch projects:', e)
  } finally {
    loading.value = false
  }
}

const loadProject = (p) => {
  projectStore.value = {
    id: p.id,
    name: p.name,
    theme: p.theme,
    keywords: p.keywords || [],
    emotions: p.emotions || [],
    product_name: p.product_name || '',
    target_audience: p.target_audience || '',
    primary_color: p.primary_color || '#000000',
    secondary_color: p.secondary_color || '#ffffff',
    niche: p.niche || '',
    logo_path: p.logo_path || '',
    context_photos: p.context_photos || [],
    references: p.references || [],
    selectedComponent: p.selected_component || 'PortraitVideo',
    componentProps: p.component_props || {}
  }
  // No need to push here, NuxtLink handles navigation
}

onMounted(() => {
  fetchProjects()
})
</script>

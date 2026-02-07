<template>
  <div class="max-w-6xl mx-auto space-y-12">
    
    <!-- Hero Section -->
    <div class="text-center py-10">
      <h1 class="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl mb-4">
        Crie Vídeos Virais com <span class="text-blue-600">Inteligência Artificial</span>
      </h1>
      <p class="max-w-2xl mx-auto text-xl text-gray-500">
        Do roteiro à edição, o Video Wizard cria conteúdo de alta conversão para sua marca em minutos.
      </p>
    </div>

    <!-- Main Action Area: Templates & New Project -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Quick Start Card -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-100 p-8 flex flex-col justify-center items-center text-center hover:shadow-xl transition-shadow lg:col-span-1">
            <div class="h-16 w-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-3xl mb-4">
                ✨
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Novo Projeto</h2>
            <p class="text-gray-500 mb-6 text-sm">Comece do zero e personalize cada detalhe do seu vídeo.</p>
            
            <div class="w-full space-y-3">
                 <input v-model="project.name" type="text" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-3 border text-center" placeholder="Nome do Projeto..." />
                 <button @click="startWizard" class="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors flex items-center justify-center gap-2">
                    <span>Criar Agora</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                 </button>
            </div>
        </div>

        <!-- Templates Library -->
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-lg border border-blue-100 p-8 lg:col-span-2">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                        🚀 Modelos Prontos
                    </h2>
                    <p class="text-sm text-gray-600">Formatos validados para alta performance.</p>
                </div>
                <!-- <button class="text-xs text-blue-600 font-semibold hover:text-blue-800">Ver Todos</button> -->
            </div>
            
            <div v-if="loadingTemplates" class="flex justify-center py-12">
                <div class="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent"></div>
            </div>
            
            <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div v-for="t in templates" :key="t.id" 
                     @click="useTemplate(t)"
                     class="group bg-white rounded-lg overflow-hidden border border-gray-200 hover:border-blue-500 hover:shadow-lg transition-all cursor-pointer relative h-40">
                    <img :src="t.thumbnail" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100" />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex flex-col justify-end p-3">
                        <h3 class="font-bold text-white text-sm leading-tight">{{ t.name }}</h3>
                        <p class="text-gray-300 text-[10px] line-clamp-1">{{ t.description }}</p>
                    </div>
                     <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <span class="bg-blue-600 text-white text-xs px-2 py-1 rounded-full font-bold shadow-sm">Usar</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Existing Projects -->
    <div v-if="projects.length > 0" class="border-t border-gray-200 pt-10">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Seus Projetos</h2>
        <button @click="refreshProjects" class="text-sm text-gray-500 hover:text-blue-600 flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          Atualizar
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="p in projects" :key="p.id" class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow cursor-pointer flex flex-col" @click="loadProject(p)">
          <div class="flex justify-between items-start mb-3">
             <div class="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center text-xl">
                 {{ p.selected_component === 'TopBottomText' ? '😂' : '🎬' }}
             </div>
             <span class="text-[10px] uppercase tracking-wider font-semibold text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {{ p.selected_component || 'Padrão' }}
             </span>
          </div>
          
          <h3 class="font-bold text-lg text-gray-900 mb-1 truncate">{{ p.name }}</h3>
          <p class="text-gray-500 text-sm mb-4 line-clamp-2">{{ p.product_name || p.theme || 'Sem descrição' }}</p>
          
          <div class="mt-auto pt-4 border-t border-gray-100 flex items-center justify-between">
             <div class="flex gap-2">
                <span v-if="p.niche" class="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">{{ p.niche }}</span>
             </div>
             <span class="text-xs text-gray-400">Editar &rarr;</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const project = useProject()
const projects = ref([])
const templates = ref([])
const loadingTemplates = ref(true)

const fetchTemplates = async () => {
  loadingTemplates.value = true
  try {
    const data = await $fetch('http://localhost:35000/templates')
    templates.value = data
  } catch (e) {
    console.error('Failed to fetch templates:', e)
  } finally {
    loadingTemplates.value = false
  }
}

const useTemplate = async (t) => {
  loadingTemplates.value = true
  try {
    const newProject = await $fetch(`http://localhost:35000/projects/from-template/${t.id}`, {
      method: 'POST'
    })
    loadProject(newProject)
  } catch (e) {
    console.error('Failed to create project from template:', e)
    alert('Failed to create project from template. Check console for details.')
    loadingTemplates.value = false
  }
}

const fetchProjects = async () => {
  try {
    const data = await $fetch('http://localhost:35000/projects')
    projects.value = data
  } catch (e) {
    console.error('Failed to fetch projects:', e)
  }
}

const refreshProjects = () => {
  fetchProjects()
}

onMounted(() => {
  fetchProjects()
  fetchTemplates()
})

const startWizard = async () => {
  // Reset state for new project
  project.value = {
    id: '',
    name: project.value.name,
    theme: project.value.theme,
    keywords: [],
    emotions: [],
    product_name: '',
    target_audience: '',
    primary_color: '#000000',
    secondary_color: '#ffffff',
    niche: '',
    logo_path: '',
    context_photos: [],
    references: [],
    selectedComponent: 'PortraitVideo',
    componentProps: {}
  }
  router.push('/wizard/step1')
}

const loadProject = (p) => {
  // Load project data into state
  project.value = {
    ...project.value, // Keep defaults for missing fields
    ...p,
    // Ensure lists are arrays (API returns them as arrays based on Pydantic models)
    keywords: p.keywords || [],
    emotions: p.emotions || [],
    context_photos: p.context_photos || [],
    references: p.references || [],
    componentProps: p.component_props || {}
  }
  
  router.push('/wizard/step1')
}
</script>
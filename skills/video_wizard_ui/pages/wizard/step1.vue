<template>
  <div class="max-w-6xl mx-auto">
    <!-- Navigation Tabs -->
    <div class="flex border-b border-gray-200 bg-white rounded-t-lg shadow-sm overflow-x-auto">
      <button 
        v-for="(step, index) in steps" 
        :key="index"
        @click="currentStep = index"
        class="flex-1 py-4 px-6 text-sm font-medium text-center focus:outline-none transition-colors whitespace-nowrap"
        :class="currentStep === index ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
      >
        <div class="flex items-center justify-center gap-2">
            <span class="flex items-center justify-center w-6 h-6 rounded-full text-xs border"
                :class="currentStep === index ? 'border-blue-600 bg-blue-100' : 'border-gray-400 bg-gray-100'">
                {{ index + 1 }}
            </span>
            {{ step.title }}
        </div>
      </button>
    </div>

    <!-- Content Area -->
    <div class="bg-white p-6 rounded-b-lg shadow-md min-h-[500px]">
        <h2 class="text-2xl font-bold mb-2">{{ steps[currentStep].title }}</h2>
        <p class="text-gray-500 mb-6">{{ steps[currentStep].description }}</p>

        <component :is="steps[currentStep].component" />
        
        <!-- Global Navigation -->
        <div class="flex justify-between mt-8 pt-6 border-t border-gray-100">
            <button 
                v-if="currentStep > 0" 
                @click="currentStep--" 
                class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-50"
            >
                ← Anterior
            </button>
            <div v-else></div>

            <button 
                v-if="currentStep < steps.length - 1" 
                @click="nextStep" 
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
                Próximo →
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import ProjectDefinition from '@/components/wizard/ProjectDefinition.vue'
import ContextAssets from '@/components/wizard/ContextAssets.vue'
import StylePreferences from '@/components/wizard/StylePreferences.vue'
import VisualSelection from '@/components/wizard/VisualSelection.vue'

const project = useProject()
const currentStep = ref(0)

const steps = [
    { title: 'Definição do Projeto', description: 'Conte sobre o seu produto e público.', component: ProjectDefinition },
    { title: 'Contexto & Arquivos', description: 'Envie logo e fotos para personalizar.', component: ContextAssets },
    { title: 'Estilo & Vibe', description: 'Escolha a estética que combina com sua marca.', component: StylePreferences },
    { title: 'Finalização & Visual', description: 'Revise e gere o seu vídeo.', component: VisualSelection },
]

const nextStep = async () => {
    // Save progress on every step transition
    await saveProject()
    if (currentStep.value < steps.length - 1) {
        currentStep.value++
    }
}

const saveProject = async () => {
    try {
        if (!project.value.id) {
            // Create if new
             const saved = await $fetch('http://localhost:35000/projects', {
                method: 'POST',
                body: project.value
            })
            project.value.id = saved.id
        } else {
            // Update
             await $fetch(`http://localhost:35000/projects/${project.value.id}`, {
                method: 'PUT',
                body: project.value
            })
        }
    } catch (e) {
        console.error("Auto-save failed", e)
    }
}
</script>

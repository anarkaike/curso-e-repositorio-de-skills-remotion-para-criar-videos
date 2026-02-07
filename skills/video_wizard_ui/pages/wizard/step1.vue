<template>
  <div class="max-w-5xl mx-auto pb-20">
    
    <!-- Wizard Header -->
    <div class="text-center py-8">
        <h1 class="text-3xl font-extrabold text-gray-900">Criador de Vídeo Inteligente</h1>
        <p class="text-gray-500 mt-2">Transforme suas ideias em vídeos profissionais em 4 passos simples.</p>
    </div>

    <!-- Stepper Navigation -->
    <div class="mb-10">
        <div class="flex items-center justify-between relative max-w-3xl mx-auto px-4">
            <!-- Connecting Line -->
            <div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-gray-200 -z-10 rounded-full"></div>
            <div class="absolute left-0 top-1/2 transform -translate-y-1/2 h-1 bg-blue-600 transition-all duration-500 rounded-full -z-10" :style="{ width: `${(currentStep / (steps.length - 1)) * 100}%` }"></div>

            <!-- Steps -->
            <div v-for="(step, index) in steps" :key="index" class="relative flex flex-col items-center group cursor-pointer" @click="currentStep = index">
                <div 
                    class="w-10 h-10 rounded-full flex items-center justify-center border-4 transition-all duration-300 bg-white z-10 font-bold"
                    :class="[
                        currentStep === index ? 'border-blue-600 text-blue-600 scale-110 shadow-lg' : 
                        currentStep > index ? 'border-blue-600 bg-blue-600 text-white' : 'border-gray-200 text-gray-400'
                    ]"
                >
                    <span v-if="currentStep > index">✓</span>
                    <span v-else>{{ index + 1 }}</span>
                </div>
                <span 
                    class="absolute -bottom-8 w-32 text-center text-xs font-semibold transition-colors duration-300"
                    :class="currentStep === index ? 'text-blue-700' : 'text-gray-400'"
                >
                    {{ step.title }}
                </span>
            </div>
        </div>
    </div>

    <!-- Content Area -->
    <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden min-h-[600px] flex flex-col">
        <!-- Step Content -->
        <div class="p-8 flex-grow">
            <transition name="fade" mode="out-in">
                <component :is="steps[currentStep].component" :key="currentStep" />
            </transition>
        </div>
        
        <!-- Footer Navigation -->
        <div class="bg-gray-50 px-8 py-6 border-t border-gray-100 flex justify-between items-center">
            <button 
                v-if="currentStep > 0" 
                @click="currentStep--" 
                class="px-6 py-2.5 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-white hover:shadow-sm transition-all flex items-center gap-2"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                Voltar
            </button>
            <div v-else>
                <button @click="$router.push('/')" class="text-gray-500 hover:text-gray-700 text-sm font-medium">Cancelar</button>
            </div>

            <button 
                v-if="currentStep < steps.length - 1" 
                @click="nextStep" 
                class="px-8 py-2.5 rounded-lg bg-blue-600 text-white font-bold hover:bg-blue-700 shadow-md hover:shadow-lg transform transition-all hover:-translate-y-0.5 flex items-center gap-2"
            >
                Próximo
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </button>
        </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

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

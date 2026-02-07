<template>
  <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4">Start New Project</h2>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Project Name</label>
        <input v-model="project.name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" placeholder="e.g. My Awesome Video" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Theme/Topic</label>
        <input v-model="project.theme" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border" placeholder="e.g. Medical Uniforms" />
      </div>
      <button @click="startWizard" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
        Next Step
      </button>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const project = useProject()

const startWizard = async () => {
  // Reset state if needed, or keep partial data
  if (!project.value.id) {
     // Could call create here, or just wait for step 1
  }
  router.push('/wizard/step1')
}
</script>

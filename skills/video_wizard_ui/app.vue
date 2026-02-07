<template>
  <div class="min-h-screen bg-gray-100 font-sans">
    <!-- Top Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-bold text-blue-600">Video Wizard AI</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink 
                to="/" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-gray-900"
              >
                Dashboard
              </NuxtLink>
              <NuxtLink 
                to="/gallery" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-gray-900"
              >
                Gallery
              </NuxtLink>
            </div>
          </div>
          <div class="flex items-center">
            <span class="text-xs text-gray-400">v0.5.0 (Beta)</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="py-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <NuxtPage />
      </div>
    </main>
  </div>
</template>

<style>
/* Global active link styling override if needed */
.router-link-active {
  /* Nuxt handles this with active-class prop usually */
}
</style>

export const useProject = () => {
  return useState('project', () => ({
    id: '',
    name: '',
    theme: '',
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
  }))
}

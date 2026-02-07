
templates = [
    {
        "id": "expert-tip",
        "name": "Dica de Especialista",
        "description": "Vídeo curto focado em entregar valor rápido. Ideal para educadores e coaches.",
        "thumbnail": "https://placehold.co/600x400/2563eb/ffffff?text=Dica+Especialista",
        "project_data": {
            "name": "Nova Dica",
            "niche": "Educação",
            "theme": "Profissional",
            "selected_component": "PortraitVideo",
            "primary_color": "#2563eb",
            "secondary_color": "#ffffff",
            "keywords": ["dica", "tutorial", "rápido"],
            "emotions": ["confiável", "direto", "útil"]
        },
        "default_script": "Você sabia que [ASSUNTO] é mais simples do que parece? O segredo é focar em [PONTO CHAVE]. Aplique isso hoje e veja a diferença!"
    },
    {
        "id": "meme-reaction",
        "name": "Meme / Reação",
        "description": "Formato viral com texto no topo e base. Ótimo para humor e identificação.",
        "thumbnail": "https://placehold.co/600x400/ca8a04/ffffff?text=Meme+Viral",
        "project_data": {
            "name": "Novo Meme",
            "niche": "Humor",
            "theme": "Descontraído",
            "selected_component": "TopBottomText",
            "primary_color": "#000000",
            "secondary_color": "#ffffff",
            "component_props": {
                "topText": "QUANDO O CLIENTE",
                "bottomText": "APROVA O ORÇAMENTO",
                "imageSrc": "https://images.unsplash.com/photo-1516251193000-18e65860f8f9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60"
            },
            "keywords": ["meme", "engraçado", "viral"],
            "emotions": ["divertido", "relatável"]
        },
        "default_script": "" # Components like TopBottomText might not use a script generation flow the same way
    },
    {
        "id": "fast-promo",
        "name": "Promoção Relâmpago",
        "description": "Anúncio de alta energia com motion blur. Ideal para ofertas limitadas.",
        "thumbnail": "https://placehold.co/600x400/dc2626/ffffff?text=Oferta+Rapida",
        "project_data": {
            "name": "Nova Promoção",
            "niche": "Vendas",
            "theme": "Urgente",
            "selected_component": "MotionBlurTitle",
            "primary_color": "#dc2626",
            "secondary_color": "#fbbf24",
            "component_props": {
                "text": "50% OFF",
                "color": "#dc2626"
            },
            "keywords": ["promoção", "desconto", "urgente"],
            "emotions": ["empolgante", "imperdível"]
        },
        "default_script": ""
    },
    {
        "id": "quote-inspiration",
        "name": "Citação Inspiradora",
        "description": "Visual cinematográfico com ruído/grão. Perfeito para frases de impacto.",
        "thumbnail": "https://placehold.co/600x400/1e293b/ffffff?text=Citacao",
        "project_data": {
            "name": "Nova Citação",
            "niche": "Motivacional",
            "theme": "Cinematográfico",
            "selected_component": "NoiseOverlay",
            "primary_color": "#ffffff",
            "secondary_color": "#000000",
            "component_props": {
                "text": "O FUTURO É AGORA",
                "noiseOpacity": 0.3
            },
            "keywords": ["inspiração", "futuro", "motivação"],
            "emotions": ["profundo", "inspirador"]
        },
        "default_script": ""
    },
    {
        "id": "product-3d",
        "name": "Lançamento Tech",
        "description": "Estilo futurista 3D. Ideal para produtos tecnológicos ou inovadores.",
        "thumbnail": "https://placehold.co/600x400/0891b2/ffffff?text=Tech+3D",
        "project_data": {
            "name": "Novo Produto",
            "niche": "Tecnologia",
            "theme": "Futurista",
            "selected_component": "ThreeDScene",
            "primary_color": "#0891b2",
            "secondary_color": "#000000",
            "component_props": {
                "text": "INOVAÇÃO",
                "primaryColor": "#0891b2"
            },
            "keywords": ["tecnologia", "inovação", "futuro"],
            "emotions": ["moderno", "avançado"]
        },
        "default_script": ""
    }
]

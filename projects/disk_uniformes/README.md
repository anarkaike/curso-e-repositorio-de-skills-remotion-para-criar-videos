# Projeto de Automação de Vídeo - Disk Uniformes

Este projeto gera vídeos automatizados para o Instagram da Disk Uniformes, utilizando scripts Python e bibliotecas como MoviePy.

## Estrutura do Projeto

- **photos/**: Contém as imagens dos produtos que aparecerão no vídeo.
  - Formatos suportados: `.jpg`, `.png`, `.webp`.
  - **Ação necessária**: Substitua as imagens numeradas (`1.png`, `2.png`, etc.) por fotos reais dos uniformes.
- **spoken_script/**: Contém o script de texto (`spoken_script.txt`) que será falado/legendado.
- **colors/**: Definições de cores para destaque nas legendas.
- **aligned_script_with_timestamps/**: Arquivo JSON com o alinhamento temporal das legendas.
- **video_output/**: Onde o vídeo final (`final_video_with_audio.mp4`) será salvo (ignorado pelo Git).
- **generate_video.sh**: Script facilitador para rodar a geração do vídeo.

## Como Gerar o Vídeo

1. Certifique-se de estar na pasta do projeto:
   ```bash
   cd projects/disk_uniformes
   ```

2. Execute o script de geração:
   ```bash
   ./generate_video.sh
   ```

3. O vídeo final estará em `video_output/final_video_with_audio.mp4`.

## Personalização

- **Alterar Imagens**: Basta substituir os arquivos na pasta `photos/`. O script ordenará as imagens alfabeticamente/numericamente.
- **Alterar Texto**: Edite `spoken_script/spoken_script.txt`. Note que se alterar o texto, será necessário gerar um novo áudio e realinhar os timestamps (JSON).
- **Alterar Cores**: Edite `colors/colors.txt` para mapear palavras-chave a cores específicas (ex: `Disk Uniformes: yellow`).

## Requisitos

Este projeto depende do ambiente virtual configurado em `../../skills/automation_lab/.venv`. O script `generate_video.sh` carrega este ambiente automaticamente.

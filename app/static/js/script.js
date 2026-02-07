document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photoInput');
    const storyContainer = document.getElementById('storyContainer');
    const loadingContainer = document.getElementById('loadingContainer');
    const buttonContainer = document.getElementById('buttonContainer');
    const actionButtons = document.getElementById('actionButtons');
    const storyTitle = document.getElementById('storyTitle');
    const storyText = document.getElementById('storyText');
    const photoDescription = document.getElementById('photoDescription');
    const newPhotoBtn = document.getElementById('newPhotoBtn');
    const saveBtn = document.getElementById('saveBtn');
    const gallerySection = document.getElementById('gallerySection');
    const storiesGallery = document.getElementById('storiesGallery');

    let currentStory = null;
    let currentImageData = null;

    // Handle photo input
    photoInput.addEventListener('change', handlePhotoUpload);
    newPhotoBtn.addEventListener('click', resetAndPhotoInput);
    saveBtn.addEventListener('click', saveStory);

    async function handlePhotoUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        // Read and convert image to base64
        const reader = new FileReader();
        reader.onload = async function(event) {
            currentImageData = event.target.result;
            
            // Determine image format from file type
            const format = file.type.split('/')[1] || 'jpeg';
            
            // Show loading, hide button
            buttonContainer.style.display = 'none';
            actionButtons.style.display = 'none';
            storyContainer.style.display = 'none';
            loadingContainer.style.display = 'flex';

            try {
                const response = await fetch('/api/generate-story', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image: currentImageData,
                        format: format
                    })
                });

                const data = await response.json();

                if (data.success) {
                    currentStory = data.story;
                    displayStory(data.story, data.title, data.description);
                    loadingContainer.style.display = 'none';
                    storyContainer.style.display = 'block';
                    actionButtons.style.display = 'flex';
                    loadGallery();
                } else {
                    showError(data.error || 'Erreur lors de la génération de l\'histoire');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Erreur lors de la communication avec le serveur');
            }
        };
        reader.readAsDataURL(file);
    }

    function displayStory(story, title, description) {
        if (title && description) {
            // New format with separate fields
            storyTitle.textContent = title;
            storyText.textContent = story;
            photoDescription.textContent = description;
        } else {
            // Fallback for older format
            const lines = story.split('\n').filter(line => line.trim() !== '');
            if (lines.length > 0) {
                const extractedTitle = lines[0].replace(/^#+\s*/, '').trim();
                const content = lines.slice(1).join('\n').trim();
                storyTitle.textContent = extractedTitle;
                storyText.textContent = content;
                photoDescription.textContent = 'Photo sans description';
            } else {
                storyTitle.textContent = 'Histoires Inattendues';
                storyText.textContent = story;
                photoDescription.textContent = 'Photo sans description';
            }
        }
    }

    function resetAndPhotoInput() {
        photoInput.value = '';
        photoInput.click();
    }

    async function saveStory() {
        if (!currentStory || !currentImageData) return;

        // For now, stories are auto-saved to Supabase from the backend
        // This button can be used for future features like sharing
        showNotification('Histoire sauvegardée !');
    }

    async function loadGallery() {
        try {
            const response = await fetch('/api/stories');
            const data = await response.json();
            
            if (data.stories && data.stories.length > 0) {
                gallerySection.style.display = 'block';
                displayGallery(data.stories);
            }
        } catch (error) {
            console.error('Error loading gallery:', error);
        }
    }

    function displayGallery(stories) {
        storiesGallery.innerHTML = '';
        
        stories.forEach((story, index) => {
            const card = document.createElement('div');
            card.className = 'story-card';
            
            // Handle both old and new formats
            const title = story.story_title || story.story_text.split('\n')[0].replace(/^#+\s*/, '').trim();
            const content = story.story_text.split('\n').slice(1).join('\n').trim();
            const description = story.photo_description || 'Photo sans description';
            const date = new Date(story.created_at).toLocaleDateString('fr-FR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            card.innerHTML = `
                <h3>${title}</h3>
                <p>${content}</p>
                <div class="date">${date}</div>
            `;
            
            card.addEventListener('click', () => {
                storyTitle.textContent = title;
                storyText.textContent = content;
                photoDescription.textContent = description;
                storyContainer.scrollIntoView({ behavior: 'smooth' });
            });
            
            storiesGallery.appendChild(card);
        });
    }

    function showError(message) {
        loadingContainer.style.display = 'none';
        buttonContainer.style.display = 'flex';
        showNotification(message);
    }

    function showNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background-color: var(--dark);
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 0.95rem;
            z-index: 1000;
            animation: slideUp 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideDown 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Add animation styles for notifications
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        
        @keyframes slideDown {
            from {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
            to {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
        }
    `;
    document.head.appendChild(style);

    // Load initial gallery on page load
    loadGallery();
});

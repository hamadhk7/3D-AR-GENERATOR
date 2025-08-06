// Main JavaScript for 3D AR Demo

// Global variables
let currentModel = null;
let scene = null;
let camera = null;
let renderer = null;
let controls = null;

// Utility functions
const utils = {
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast show bg-${type} text-white`;
        toast.innerHTML = `
            <div class="toast-body">
                ${message}
            </div>
        `;
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    },

    // Show loading state
    showLoading: function(element) {
        if (!element) return;
        element.disabled = true;
        element.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
    },

    // Hide loading state
    hideLoading: function(element, originalText) {
        if (!element) return;
        element.disabled = false;
        element.innerHTML = originalText;
    },

    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
};

// API functions
const api = {
    // Get models list
    getModels: async function(limit = null) {
        try {
            const url = limit ? `/api/models?limit=${limit}` : '/api/models';
            const response = await fetch(url);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching models:', error);
            utils.showToast('Failed to load models', 'danger');
            return [];
        }
    },

    // Generate new model
    generateModel: async function(prompt) {
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error generating model:', error);
            utils.showToast('Failed to generate model', 'danger');
            return null;
        }
    },

    // Get model details
    getModel: async function(modelId) {
        try {
            const response = await fetch(`/api/models/${modelId}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching model:', error);
            utils.showToast('Failed to load model details', 'danger');
            return null;
        }
    }
};

// 3D Model Viewer
class ModelViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.model = null;
        this.animationId = null;
        
        this.init();
    }

    init() {
        if (!this.container) return;

        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f0f0);

        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 0, 5);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Add controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;

        // Add lights
        this.addLights();

        // Start animation loop
        this.animate();

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    addLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);

        // Point light
        const pointLight = new THREE.PointLight(0xffffff, 0.5);
        pointLight.position.set(-10, -10, -5);
        this.scene.add(pointLight);
    }

    loadModel(modelPath) {
        const loader = new THREE.GLTFLoader();
        
        loader.load(
            modelPath,
            (gltf) => {
                // Remove previous model
                if (this.model) {
                    this.scene.remove(this.model);
                }

                this.model = gltf.scene;
                this.scene.add(this.model);

                // Center and scale model
                const box = new THREE.Box3().setFromObject(this.model);
                const center = box.getCenter(new THREE.Vector3());
                const size = box.getSize(new THREE.Vector3());
                
                const maxDim = Math.max(size.x, size.y, size.z);
                const scale = 2 / maxDim;
                this.model.scale.setScalar(scale);
                
                this.model.position.sub(center.multiplyScalar(scale));

                utils.showToast('Model loaded successfully', 'success');
            },
            (progress) => {
                console.log('Loading progress:', (progress.loaded / progress.total * 100) + '%');
            },
            (error) => {
                console.error('Error loading model:', error);
                utils.showToast('Failed to load model', 'danger');
            }
        );
    }

    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        if (this.controls) {
            this.controls.update();
        }
        
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }

    onWindowResize() {
        if (this.camera && this.renderer && this.container) {
            this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        }
    }

    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// AR Viewer
class ARViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.video = null;
        this.canvas = null;
        this.ctx = null;
        this.isARSupported = false;
        
        this.init();
    }

    async init() {
        if (!this.container) return;

        // Check AR support
        this.isARSupported = await this.checkARSupport();
        
        if (!this.isARSupported) {
            this.showARNotSupported();
            return;
        }

        this.setupAR();
    }

    async checkARSupport() {
        // Check for WebXR support
        if ('xr' in navigator) {
            return await navigator.xr.isSessionSupported('immersive-ar');
        }
        return false;
    }

    showARNotSupported() {
        this.container.innerHTML = `
            <div class="text-center p-5">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h4>AR Not Supported</h4>
                <p>Your device or browser doesn't support AR features.</p>
                <p>Please try using a compatible mobile device with ARCore (Android) or ARKit (iOS).</p>
            </div>
        `;
    }

    setupAR() {
        // Create video element
        this.video = document.createElement('video');
        this.video.style.display = 'none';
        this.container.appendChild(this.video);

        // Create canvas
        this.canvas = document.createElement('canvas');
        this.canvas.className = 'ar-canvas';
        this.container.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');

        // Add AR controls
        this.addARControls();
    }

    addARControls() {
        const controls = document.createElement('div');
        controls.className = 'ar-controls position-absolute top-0 start-0 p-3';
        controls.innerHTML = `
            <button class="btn btn-primary btn-sm me-2" onclick="arViewer.startAR()">
                <i class="fas fa-play me-1"></i>Start AR
            </button>
            <button class="btn btn-secondary btn-sm" onclick="arViewer.stopAR()">
                <i class="fas fa-stop me-1"></i>Stop AR
            </button>
        `;
        this.container.appendChild(controls);
    }

    async startAR() {
        try {
            const session = await navigator.xr.requestSession('immersive-ar');
            utils.showToast('AR session started', 'success');
            // AR session handling would go here
        } catch (error) {
            console.error('Error starting AR:', error);
            utils.showToast('Failed to start AR session', 'danger');
        }
    }

    stopAR() {
        // Stop AR session
        utils.showToast('AR session stopped', 'info');
    }
}

// Form handlers
const formHandlers = {
    // Model generation form
    handleGenerateForm: function(form) {
        const submitBtn = document.getElementById('generateBtn');
        const generateBtnText = document.getElementById('generateBtnText');
        const progressDiv = document.getElementById('generationProgress');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const progressStatus = document.getElementById('progressStatus');
        const promptInput = form.querySelector('textarea[name="prompt"]');
        const prompt = promptInput.value.trim();

        if (!prompt) {
            utils.showToast('Please enter a prompt', 'warning');
            return;
        }

        // Show progress UI
        submitBtn.disabled = true;
        generateBtnText.textContent = 'Generating...';
        progressDiv.style.display = 'block';
        
        // Start progress simulation
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90; // Don't go to 100% until we get response
            
            progressBar.style.width = progress + '%';
            progressBar.setAttribute('aria-valuenow', progress);
            progressText.textContent = Math.round(progress) + '%';
            
            // Update status text based on progress
            if (progress < 20) {
                progressStatus.textContent = 'Initializing generation...';
            } else if (progress < 40) {
                progressStatus.textContent = 'Processing your prompt...';
            } else if (progress < 60) {
                progressStatus.textContent = 'Creating 3D geometry...';
            } else if (progress < 80) {
                progressStatus.textContent = 'Applying textures and materials...';
            } else {
                progressStatus.textContent = 'Finalizing model...';
            }
        }, 500);

        api.generateModel(prompt)
            .then(result => {
                // Complete the progress
                clearInterval(progressInterval);
                progressBar.style.width = '100%';
                progressBar.setAttribute('aria-valuenow', 100);
                progressText.textContent = '100%';
                progressStatus.textContent = 'Generation complete!';
                
                if (result && result.success) {
                    utils.showToast(result.message || 'Model generation started!', 'success');
                    promptInput.value = '';
                    
                    // Show completion for 2 seconds, then reload
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                } else {
                    utils.showToast(result?.error || 'Failed to generate model', 'danger');
                    // Reset UI on error
                    submitBtn.disabled = false;
                    generateBtnText.textContent = 'Generate Model';
                    progressDiv.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                utils.showToast('Network error occurred', 'danger');
                // Reset UI on error
                clearInterval(progressInterval);
                submitBtn.disabled = false;
                generateBtnText.textContent = 'Generate Model';
                progressDiv.style.display = 'none';
            });
    }
};

// Model loading functions
async function loadModels(limit = null) {
    const modelsContainer = document.getElementById('models-container');
    if (!modelsContainer) return;

    const models = await api.getModels(limit);
    
    if (models.length === 0) {
        modelsContainer.innerHTML = `
            <div class="text-center p-5">
                <i class="fas fa-cube fa-3x text-muted mb-3"></i>
                <h4>No Models Found</h4>
                <p>Generate your first 3D model to get started!</p>
            </div>
        `;
        return;
    }

    const modelsHTML = models.map(model => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card model-card h-100" onclick="viewModel('${model.id}')">
                <div class="card-body text-center">
                    <i class="fas fa-cube fa-3x text-primary mb-3"></i>
                    <h5 class="card-title">${model.name}</h5>
                    <p class="card-text text-muted">${model.description || 'No description'}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">${utils.formatDate(model.created_at)}</small>
                        <span class="badge bg-primary">${model.status}</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    modelsContainer.innerHTML = modelsHTML;
}

async function viewModel(modelId) {
    window.location.href = `/view/${modelId}`;
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form handlers
    const generateForm = document.getElementById('generationForm');
    if (generateForm) {
        generateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            formHandlers.handleGenerateForm(this);
        });
    }

    // Initialize model viewer if on model view page
    const modelViewerContainer = document.getElementById('model-viewer');
    if (modelViewerContainer) {
        window.modelViewer = new ModelViewer('model-viewer');
        
        // Load model if modelId is available
        const modelId = modelViewerContainer.dataset.modelId;
        if (modelId) {
            loadModelForViewer(modelId);
        }
    }

    // Initialize AR viewer if on AR page
    const arViewerContainer = document.getElementById('ar-viewer');
    if (arViewerContainer) {
        window.arViewer = new ARViewer('ar-viewer');
    }

    // Load models on home page
    const modelsContainer = document.getElementById('models-container');
    if (modelsContainer) {
        loadModels(6); // Load 6 models for home page
    }
});

// Load model for viewer
async function loadModelForViewer(modelId) {
    const model = await api.getModel(modelId);
    if (model && model.glb_url && window.modelViewer) {
        window.modelViewer.loadModel(model.glb_url);
    }
}

// Load credits function
async function loadCredits() {
    try {
        const response = await fetch('/api/credits');
        const data = await response.json();
        
        if (data.success) {
            // Update credit display elements
            const apiWallet = document.getElementById('apiWallet');
            const freeWallet = document.getElementById('freeWallet');
            const totalUsed = document.getElementById('totalUsed');
            const creditNote = document.getElementById('creditNote');
            
            if (apiWallet) apiWallet.textContent = data.api_wallet || 0;
            if (freeWallet) freeWallet.textContent = data.free_wallet || 0;
            if (totalUsed) totalUsed.textContent = data.total_used || 0;
            if (creditNote) creditNote.textContent = data.note || '';
            
            // Update badge colors based on source
            if (data.source === 'user_account' || data.source === 'real_tripo_api') {
                if (apiWallet) apiWallet.className = 'badge bg-success fs-6';
                if (freeWallet) freeWallet.className = 'badge bg-success fs-6';
            }
        }
    } catch (error) {
        console.error('Error loading credits:', error);
    }
}

// Export for global access
window.utils = utils;
window.api = api;
window.loadModels = loadModels;
window.viewModel = viewModel;
window.loadCredits = loadCredits;

// Add loadRecentModels function for the home page
window.loadRecentModels = function() {
    fetch('/api/models?limit=6')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('recentModels');
            if (!container) return;
            
            if (data.models && data.models.length > 0) {
                container.innerHTML = data.models.map(model => `
                    <div class="col-md-4 col-lg-3 mb-3">
                        <div class="card model-card h-100" onclick="viewModel('${model.id}')">
                            <div class="card-body text-center">
                                <div class="mb-3">
                                    <i class="fas fa-cube fa-2x text-primary"></i>
                                </div>
                                <h6 class="card-title">${model.prompt.substring(0, 50)}${model.prompt.length > 50 ? '...' : ''}</h6>
                                <p class="card-text small text-muted">
                                    <i class="fas fa-file me-1"></i>${model.format.toUpperCase()}
                                    <br>
                                    <i class="fas fa-calendar me-1"></i>${new Date(model.created_at).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-muted">No models generated yet. Create your first model above!</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error loading models:', error);
            const container = document.getElementById('recentModels');
            if (container) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-danger">Failed to load models</p>
                    </div>
                `;
            }
        });
}; 
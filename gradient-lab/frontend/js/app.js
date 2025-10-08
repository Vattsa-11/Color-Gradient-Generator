/**
 * Gradient Lab - Color Gradient Generator
 * Main JavaScript application logic
 */

class GradientLab {
    constructor() {
        this.state = {
            stops: [
                { color: '#FF6B6B', position: 0 },
                { color: '#FFD93D', position: 50 },
                { color: '#6BCB77', position: 100 }
            ],
            type: 'linear',
            angle: 90,
            space: 'hsl',
            steps: 32,
            theme: this.getPreferredTheme()
        };

        this.debounceTimer = null;
        this.draggedElement = null;
        
        this.init();
    }

    init() {
        console.log('Gradient Lab initializing...');
        
        try {
            this.loadState();
            console.log('State loaded');
            
            this.applyTheme();
            console.log('Theme applied');
            
            this.renderColorStops();
            console.log('Color stops rendered');
            
            this.setupEventListeners();
            console.log('Event listeners set up');
            
            // Show immediate fallback preview
            this.setFallbackPreview();
            console.log('Fallback preview set');
            
            // Load enhanced preview with a small delay to allow page to render first
            setTimeout(() => {
                console.log('Starting API preview update...');
                this.updatePreview();
            }, 100);
            
            console.log('Gradient Lab initialization complete');
        } catch (error) {
            console.error('Error during initialization:', error);
        }
    }

    setupEventListeners() {
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Color stops
        document.getElementById('add-stop').addEventListener('click', () => {
            this.addColorStop();
        });

        // Gradient settings
        document.getElementById('gradient-type').addEventListener('change', (e) => {
            this.state.type = e.target.value;
            this.updateAngleVisibility();
            this.debouncedUpdate();
        });

        document.getElementById('angle-slider').addEventListener('input', (e) => {
            this.state.angle = parseInt(e.target.value);
            document.getElementById('angle-value').textContent = `${this.state.angle}°`;
            this.debouncedUpdate();
        });

        document.getElementById('color-space').addEventListener('change', (e) => {
            this.state.space = e.target.value;
            this.debouncedUpdate();
        });

        document.getElementById('steps-slider').addEventListener('input', (e) => {
            this.state.steps = parseInt(e.target.value);
            document.getElementById('steps-value').textContent = this.state.steps;
            this.debouncedUpdate();
        });

        // Quick actions
        document.getElementById('randomize-btn').addEventListener('click', () => {
            this.randomizeColors();
        });

        document.getElementById('reverse-btn').addEventListener('click', () => {
            this.reverseStops();
        });

        document.getElementById('equalize-btn').addEventListener('click', () => {
            this.equalizeStops();
        });

        // Export
        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportImage();
        });

        // Copy CSS
        document.getElementById('copy-css-btn').addEventListener('click', () => {
            this.copyCSSToClipboard();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'r':
                        e.preventDefault();
                        this.randomizeColors();
                        break;
                    case 'e':
                        e.preventDefault();
                        this.equalizeStops();
                        break;
                    case 'c':
                        if (e.target.id === 'css-output') {
                            // Let default copy behavior work
                            return;
                        }
                        e.preventDefault();
                        this.copyCSSToClipboard();
                        break;
                }
            }
        });

        // Initial angle visibility
        this.updateAngleVisibility();
    }

    getPreferredTheme() {
        const stored = localStorage.getItem('gradient-lab-theme');
        if (stored) return stored;
        
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    toggleTheme() {
        this.state.theme = this.state.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
        this.saveState();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.state.theme);
        const themeIcon = document.querySelector('.theme-icon');
        themeIcon.textContent = this.state.theme === 'light' ? '🌙' : '☀️';
    }

    loadState() {
        const saved = localStorage.getItem('gradient-lab-state');
        if (saved) {
            try {
                const parsedState = JSON.parse(saved);
                this.state = { ...this.state, ...parsedState };
                
                // Update UI elements
                document.getElementById('gradient-type').value = this.state.type;
                document.getElementById('angle-slider').value = this.state.angle;
                document.getElementById('angle-value').textContent = `${this.state.angle}°`;
                document.getElementById('color-space').value = this.state.space;
                document.getElementById('steps-slider').value = this.state.steps;
                document.getElementById('steps-value').textContent = this.state.steps;
            } catch (e) {
                console.warn('Failed to load saved state:', e);
            }
        }
    }

    saveState() {
        localStorage.setItem('gradient-lab-state', JSON.stringify(this.state));
        localStorage.setItem('gradient-lab-theme', this.state.theme);
    }

    renderColorStops() {
        const container = document.getElementById('color-stops');
        container.innerHTML = '';

        this.state.stops.forEach((stop, index) => {
            const stopElement = this.createColorStopElement(stop, index);
            container.appendChild(stopElement);
        });
    }

    createColorStopElement(stop, index) {
        const div = document.createElement('div');
        div.className = 'color-stop';
        div.setAttribute('role', 'listitem');
        div.innerHTML = `
            <div class="color-stop-drag" title="Drag to reorder">⋮⋮</div>
            <input 
                type="color" 
                class="color-input" 
                value="${stop.color}"
                aria-label="Color ${index + 1}"
                title="Choose color">
            <div class="position-control">
                <div class="position-label">${stop.position.toFixed(1)}%</div>
                <input 
                    type="range" 
                    class="position-slider form-range" 
                    min="0" 
                    max="100" 
                    step="0.1"
                    value="${stop.position}"
                    aria-label="Position percentage">
            </div>
            ${this.state.stops.length > 2 ? `
                <button 
                    class="delete-stop" 
                    title="Delete color stop"
                    aria-label="Delete color stop ${index + 1}">
                    ×
                </button>
            ` : ''}
        `;

        // Event listeners
        const colorInput = div.querySelector('.color-input');
        const positionSlider = div.querySelector('.position-slider');
        const deleteBtn = div.querySelector('.delete-stop');
        const positionLabel = div.querySelector('.position-label');

        colorInput.addEventListener('input', (e) => {
            this.state.stops[index].color = e.target.value.toUpperCase();
            this.debouncedUpdate();
        });

        positionSlider.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            this.state.stops[index].position = value;
            positionLabel.textContent = `${value.toFixed(1)}%`;
            this.debouncedUpdate();
        });

        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                this.removeColorStop(index);
            });
        }

        // Drag and drop (simplified version)
        this.setupDragAndDrop(div, index);

        return div;
    }

    setupDragAndDrop(element, index) {
        const dragHandle = element.querySelector('.color-stop-drag');
        
        dragHandle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            this.startDrag(element, index, e);
        });

        // Touch support
        dragHandle.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startDrag(element, index, e.touches[0]);
        });
    }

    startDrag(element, index, event) {
        this.draggedElement = { element, index };
        const container = document.getElementById('color-stops');
        
        // Add visual feedback
        element.style.opacity = '0.5';
        element.style.transform = 'scale(1.05)';
        
        const mouseMoveHandler = (e) => {
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (!clientY) return;
            
            const elements = [...container.children];
            const draggedRect = element.getBoundingClientRect();
            let targetIndex = index;
            
            elements.forEach((el, idx) => {
                if (el === element) return;
                const rect = el.getBoundingClientRect();
                const midpoint = rect.top + rect.height / 2;
                
                if (clientY < midpoint && idx < index) {
                    targetIndex = idx;
                } else if (clientY > midpoint && idx > index) {
                    targetIndex = idx;
                }
            });
            
            if (targetIndex !== index) {
                this.moveColorStop(index, targetIndex);
                this.renderColorStops();
                this.debouncedUpdate();
            }
        };
        
        const mouseUpHandler = () => {
            element.style.opacity = '';
            element.style.transform = '';
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
            document.removeEventListener('touchmove', mouseMoveHandler);
            document.removeEventListener('touchend', mouseUpHandler);
            this.draggedElement = null;
        };
        
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
        document.addEventListener('touchmove', mouseMoveHandler);
        document.addEventListener('touchend', mouseUpHandler);
    }

    addColorStop() {
        if (this.state.stops.length >= 12) {
            this.showToast('Maximum of 12 color stops allowed', 'warning');
            return;
        }

        // Find a good position for the new stop
        const positions = this.state.stops.map(s => s.position).sort((a, b) => a - b);
        let newPosition = 50;
        
        // Find the largest gap between stops
        let maxGap = 0;
        let gapPosition = 50;
        
        for (let i = 0; i < positions.length - 1; i++) {
            const gap = positions[i + 1] - positions[i];
            if (gap > maxGap) {
                maxGap = gap;
                gapPosition = positions[i] + gap / 2;
            }
        }
        
        if (maxGap > 10) {
            newPosition = gapPosition;
        }

        // Generate a harmonious color
        const newColor = this.generateHarmoniousColor();
        
        this.state.stops.push({
            color: newColor,
            position: newPosition
        });

        this.renderColorStops();
        this.debouncedUpdate();
        this.showToast('Color stop added', 'success');
    }

    removeColorStop(index) {
        if (this.state.stops.length <= 2) {
            this.showToast('Minimum of 2 color stops required', 'warning');
            return;
        }

        this.state.stops.splice(index, 1);
        this.renderColorStops();
        this.debouncedUpdate();
        this.showToast('Color stop removed', 'success');
    }

    moveColorStop(fromIndex, toIndex) {
        const stop = this.state.stops.splice(fromIndex, 1)[0];
        this.state.stops.splice(toIndex, 0, stop);
    }

    randomizeColors() {
        // Generate harmonious color palette
        const hues = this.generateHarmoniousHues(this.state.stops.length);
        const saturation = 70 + Math.random() * 20; // 70-90%
        const lightness = 45 + Math.random() * 20; // 45-65%

        this.state.stops.forEach((stop, index) => {
            stop.color = this.hslToHex(hues[index], saturation, lightness);
        });

        this.renderColorStops();
        this.debouncedUpdate();
        this.showToast('Colors randomized', 'success');
    }

    generateHarmoniousHues(count) {
        const baseHue = Math.random() * 360;
        const hues = [];
        
        if (count <= 3) {
            // Triadic or complementary
            for (let i = 0; i < count; i++) {
                hues.push((baseHue + (i * 120)) % 360);
            }
        } else {
            // Analogous with some variation
            const spread = Math.min(180, count * 30);
            for (let i = 0; i < count; i++) {
                const offset = (i / (count - 1) - 0.5) * spread;
                hues.push((baseHue + offset + 360) % 360);
            }
        }
        
        return hues;
    }

    generateHarmoniousColor() {
        // Generate a color that works well with existing colors
        const existingHues = this.state.stops.map(stop => {
            const rgb = this.hexToRgb(stop.color);
            return this.rgbToHsl(rgb.r, rgb.g, rgb.b).h;
        });

        const avgHue = existingHues.reduce((sum, hue) => sum + hue, 0) / existingHues.length;
        const newHue = (avgHue + 120 + Math.random() * 60 - 30) % 360;
        
        return this.hslToHex(newHue, 70 + Math.random() * 20, 50 + Math.random() * 20);
    }

    reverseStops() {
        // Reverse the color order but keep positions
        const colors = this.state.stops.map(s => s.color).reverse();
        this.state.stops.forEach((stop, index) => {
            stop.color = colors[index];
        });

        this.renderColorStops();
        this.debouncedUpdate();
        this.showToast('Colors reversed', 'success');
    }

    equalizeStops() {
        // Distribute stops evenly
        this.state.stops.forEach((stop, index) => {
            stop.position = (index / (this.state.stops.length - 1)) * 100;
        });

        this.renderColorStops();
        this.debouncedUpdate();
        this.showToast('Stops equalized', 'success');
    }

    updateAngleVisibility() {
        const angleGroup = document.getElementById('angle-group');
        const shouldShow = this.state.type === 'linear' || this.state.type === 'conic';
        angleGroup.style.display = shouldShow ? 'block' : 'none';
    }

    debouncedUpdate() {
        // Show immediate fallback preview
        this.setFallbackPreview();
        
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.updatePreview();
            this.saveState();
        }, 150);
    }

    async updatePreview() {
        try {
            // Create an AbortController for timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const response = await fetch('/api/gradient', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    stops: this.state.stops,
                    steps: this.state.steps,
                    space: this.state.space,
                    type: this.state.type,
                    angle: this.state.angle
                }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate gradient');
            }

            const data = await response.json();
            
            // Update preview
            const preview = document.getElementById('gradient-preview');
            preview.style.background = data.css.replace('background: ', '');
            
            // Update CSS output
            document.getElementById('css-output').value = data.css;
            
            // Update contrast check
            this.updateContrastCheck(data.colors);
            
        } catch (error) {
            console.error('Failed to update preview:', error);
            this.showToast(error.message, 'error');
            // Keep the fallback preview if API fails
        }
    }

    setFallbackPreview() {
        console.log('Setting fallback preview...');
        console.log('Current state:', this.state);
        
        try {
            // Generate a basic CSS gradient without API call for immediate feedback
            const stops = this.state.stops.map(stop => 
                `${stop.color} ${stop.position}%`
            ).join(', ');
            
            console.log('Generated stops:', stops);
            
            let cssGradient;
            if (this.state.type === 'linear') {
                cssGradient = `linear-gradient(${this.state.angle}deg, ${stops})`;
            } else if (this.state.type === 'radial') {
                cssGradient = `radial-gradient(circle, ${stops})`;
            } else if (this.state.type === 'conic') {
                cssGradient = `conic-gradient(from ${this.state.angle}deg, ${stops})`;
            }
            
            console.log('Generated CSS gradient:', cssGradient);
            
            const preview = document.getElementById('gradient-preview');
            if (preview) {
                preview.style.background = cssGradient;
                console.log('Preview element updated');
            } else {
                console.error('Preview element not found!');
            }
            
            const cssOutput = document.getElementById('css-output');
            if (cssOutput) {
                cssOutput.value = `background: ${cssGradient};`;
                console.log('CSS output updated');
            } else {
                console.error('CSS output element not found!');
            }
        } catch (error) {
            console.error('Error in setFallbackPreview:', error);
        }
    }

    updateContrastCheck(colors) {
        // Check contrast with white text
        const badge = document.getElementById('contrast-badge');
        const midColor = colors[Math.floor(colors.length / 2)];
        const contrastRatio = this.calculateContrastRatio('#FFFFFF', midColor);
        
        const isGoodContrast = contrastRatio >= 4.5; // WCAG AA standard
        badge.className = `contrast-badge ${isGoodContrast ? 'pass' : 'fail'}`;
        badge.textContent = isGoodContrast ? 'AA ✓' : 'AA ✗';
        badge.title = `Contrast ratio: ${contrastRatio.toFixed(2)}:1`;
    }

    async exportImage() {
        const width = parseInt(document.getElementById('export-width').value);
        const height = parseInt(document.getElementById('export-height').value);
        
        if (width < 32 || width > 8192 || height < 32 || height > 8192) {
            this.showToast('Invalid dimensions. Use values between 32 and 8192.', 'error');
            return;
        }

        this.showLoading(true);
        
        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    stops: this.state.stops,
                    steps: 256, // High quality for export
                    space: this.state.space,
                    type: this.state.type,
                    angle: this.state.angle,
                    width: width,
                    height: height,
                    format: 'png'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to export image');
            }

            // Download the file
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `gradient_${this.state.type}_${width}x${height}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.showToast('Image exported successfully', 'success');
            
        } catch (error) {
            console.error('Failed to export image:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async copyCSSToClipboard() {
        const cssOutput = document.getElementById('css-output');
        
        try {
            await navigator.clipboard.writeText(cssOutput.value);
            this.showToast('CSS copied to clipboard', 'success');
        } catch (error) {
            // Fallback for older browsers
            cssOutput.select();
            document.execCommand('copy');
            this.showToast('CSS copied to clipboard', 'success');
        }
    }

    showLoading(show) {
        const indicator = document.getElementById('loading-indicator');
        indicator.classList.toggle('visible', show);
        indicator.setAttribute('aria-hidden', !show);
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }

    // Color utility functions
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    rgbToHsl(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;

        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0;
        } else {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

            switch (max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
            }
            h /= 6;
        }

        return { h: h * 360, s: s * 100, l: l * 100 };
    }

    hslToHex(h, s, l) {
        h = ((h % 360) + 360) % 360;
        s = Math.max(0, Math.min(100, s)) / 100;
        l = Math.max(0, Math.min(100, l)) / 100;

        const c = (1 - Math.abs(2 * l - 1)) * s;
        const x = c * (1 - Math.abs((h / 60) % 2 - 1));
        const m = l - c / 2;
        let r = 0, g = 0, b = 0;

        if (0 <= h && h < 60) {
            r = c; g = x; b = 0;
        } else if (60 <= h && h < 120) {
            r = x; g = c; b = 0;
        } else if (120 <= h && h < 180) {
            r = 0; g = c; b = x;
        } else if (180 <= h && h < 240) {
            r = 0; g = x; b = c;
        } else if (240 <= h && h < 300) {
            r = x; g = 0; b = c;
        } else if (300 <= h && h < 360) {
            r = c; g = 0; b = x;
        }

        r = Math.round((r + m) * 255);
        g = Math.round((g + m) * 255);
        b = Math.round((b + m) * 255);

        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
    }

    calculateContrastRatio(color1, color2) {
        const getLuminance = (hex) => {
            const rgb = this.hexToRgb(hex);
            const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(c => {
                c = c / 255;
                return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        };

        const lum1 = getLuminance(color1);
        const lum2 = getLuminance(color2);
        const brightest = Math.max(lum1, lum2);
        const darkest = Math.min(lum1, lum2);

        return (brightest + 0.05) / (darkest + 0.05);
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing Gradient Lab...');
    try {
        new GradientLab();
    } catch (error) {
        console.error('Failed to initialize Gradient Lab:', error);
        // Show a simple fallback
        const preview = document.getElementById('gradient-preview');
        if (preview) {
            preview.style.background = 'linear-gradient(90deg, #ff6b6b 0%, #ffd93d 50%, #6bcb77 100%)';
            preview.innerHTML = '<div style="color: white; padding: 20px; text-align: center;">Gradient Lab (Basic Mode)<br>Check console for errors</div>';
        }
    }
});
// ============================================
// LLM Router - Frontend Application
// ============================================

class LLMRouterApp {
    constructor() {
        this.currentProvider = null;
        this.currentModel = null;
        this.isProcessing = false;
        this.providers = [];

        this.init();
    }

    init() {
        // Get DOM elements
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.providerSelect = document.getElementById('provider-select');
        this.providerStatus = document.getElementById('provider-status');
        this.routingInfo = document.getElementById('routing-info');
        this.providerCount = document.getElementById('provider-count');
        this.totalCost = document.getElementById('total-cost');

        // Set up event listeners
        this.setupEventListeners();

        // Load initial data
        this.loadProviders();

        // Auto-resize textarea
        this.setupTextareaAutoResize();
    }

    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Enter key to send (Shift+Enter for new line)
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    setupTextareaAutoResize() {
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = this.userInput.scrollHeight + 'px';
        });
    }

    async loadProviders() {
        try {
            const response = await fetch('/api/providers');
            const data = await response.json();

            this.providers = data.providers;
            this.updateProviderStatus(data.stats);
            this.updateProviderSelect(data.providers);
            this.updateProviderCount(data.providers.length);

        } catch (error) {
            console.error('Error loading providers:', error);
            this.showError('Failed to load providers');
        }
    }

    updateProviderStatus(stats) {
        if (!stats || stats.length === 0) {
            this.providerStatus.innerHTML = `
                <div class="error-message">
                    No providers configured. Please add API keys to .env file.
                </div>
            `;
            return;
        }

        this.providerStatus.innerHTML = stats.map(stat => {
            const isAvailable = stat.available;
            const statusClass = isAvailable ? '' : 'error';
            const itemClass = isAvailable ? '' : 'unavailable';

            let content = `
                <div class="provider-item ${itemClass}">
                    <div class="provider-header">
                        <span class="provider-name">${stat.provider}</span>
                        <span class="provider-status ${statusClass}"></span>
                    </div>
                    <div class="provider-model">${stat.model}</div>
            `;

            if (isAvailable) {
                content += `
                    <div class="provider-stats">
                        <div class="provider-stat">
                            Requests: <strong>${stat.request_count}</strong>
                        </div>
                        <div class="provider-stat">
                            Cost: <strong>$${stat.total_cost}</strong>
                        </div>
                    </div>
                `;
            } else {
                content += `
                    <div class="provider-error">
                        ${stat.error || 'Not available'}
                    </div>
                `;
            }

            content += `</div>`;
            return content;
        }).join('');

        // Update total cost (only from available providers)
        const totalCost = stats
            .filter(stat => stat.available)
            .reduce((sum, stat) => sum + stat.total_cost, 0);
        this.totalCost.textContent = `$${totalCost.toFixed(4)}`;

        // Update provider count (only available providers)
        const availableCount = stats.filter(stat => stat.available).length;
        this.providerCount.textContent = availableCount;
    }

    updateProviderSelect(providers) {
        // Clear existing options except the first one (Auto)
        this.providerSelect.innerHTML = '<option value="">Auto (Smart Routing)</option>';

        // Add provider options
        providers.forEach(provider => {
            const option = document.createElement('option');
            option.value = provider;
            option.textContent = provider.charAt(0).toUpperCase() + provider.slice(1);
            this.providerSelect.appendChild(option);
        });
    }

    updateProviderCount(count) {
        this.providerCount.textContent = count;
    }

    async sendMessage() {
        const query = this.userInput.value.trim();

        if (!query || this.isProcessing) {
            return;
        }

        // Clear input
        this.userInput.value = '';
        this.userInput.style.height = 'auto';

        // Disable input
        this.isProcessing = true;
        this.sendButton.disabled = true;
        this.userInput.disabled = true;

        // Add user message to chat
        this.addUserMessage(query);

        // Get selected provider preference
        const preferredProvider = this.providerSelect.value || null;

        // Create assistant message placeholder
        const assistantMessageId = this.addAssistantMessage('');

        try {
            await this.streamResponse(query, preferredProvider, assistantMessageId);
        } catch (error) {
            console.error('Error:', error);
            this.updateAssistantMessage(assistantMessageId, 'Sorry, an error occurred. Please try again.');
        } finally {
            // Re-enable input
            this.isProcessing = false;
            this.sendButton.disabled = false;
            this.userInput.disabled = false;
            this.userInput.focus();

            // Reload provider stats
            this.loadProviders();
        }
    }

    async streamResponse(query, preferredProvider, messageId) {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                provider: preferredProvider
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullResponse = '';
        let routingData = null;
        let selectedProvider = null;
        let selectedModel = null;

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const event = JSON.parse(line.slice(6));

                        if (event.type === 'routing') {
                            routingData = event.data;
                            this.updateRoutingInfo(routingData);
                        } else if (event.type === 'provider') {
                            if (event.data.status === 'success') {
                                selectedProvider = event.data.provider;
                                selectedModel = event.data.model;
                            } else if (event.data.status === 'attempting') {
                                this.updateAssistantMessage(
                                    messageId,
                                    `Trying ${event.data.provider}...`,
                                    event.data.provider,
                                    event.data.model
                                );
                            }
                        } else if (event.type === 'content') {
                            fullResponse += event.data;
                            this.updateAssistantMessage(
                                messageId,
                                fullResponse,
                                selectedProvider,
                                selectedModel
                            );
                        } else if (event.type === 'error') {
                            if (event.data.attempting_fallback) {
                                // Show fallback attempt
                                console.log(`Provider ${event.data.provider} failed, trying fallback...`);
                            } else {
                                // Final error
                                this.updateAssistantMessage(
                                    messageId,
                                    `Error: ${event.data.error}`,
                                    null,
                                    null
                                );
                            }
                        } else if (event.type === 'complete') {
                            // Response complete
                            console.log('Response complete:', event.data);
                        }
                    } catch (e) {
                        console.error('Error parsing SSE:', e);
                    }
                }
            }
        }
    }

    addUserMessage(text) {
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <div class="message-bubble">${this.escapeHtml(text)}</div>
                <div class="message-meta">
                    <span>${this.getCurrentTime()}</span>
                </div>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addAssistantMessage(text) {
        const messageId = 'msg-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.id = messageId;
        messageDiv.className = 'message assistant';
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                <div class="message-meta"></div>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();

        return messageId;
    }

    updateAssistantMessage(messageId, text, provider, model) {
        const messageDiv = document.getElementById(messageId);
        if (!messageDiv) return;

        const bubble = messageDiv.querySelector('.message-bubble');
        const meta = messageDiv.querySelector('.message-meta');

        // Update content
        bubble.innerHTML = this.formatMessage(text);

        // Update metadata
        let metaHtml = `<span>${this.getCurrentTime()}</span>`;
        if (provider) {
            metaHtml += `<span class="provider-badge ${provider}">${provider}</span>`;
        }
        meta.innerHTML = metaHtml;

        this.scrollToBottom();
    }

    updateRoutingInfo(routingData) {
        const { provider, model, reason, query_metadata } = routingData;

        this.routingInfo.innerHTML = `
            <div class="routing-detail">
                <div class="routing-detail-item">
                    <span class="routing-label">Selected Provider</span>
                    <span class="routing-value">${provider || 'None'}</span>
                </div>
                <div class="routing-detail-item">
                    <span class="routing-label">Model</span>
                    <span class="routing-value">${model || 'N/A'}</span>
                </div>
                <div class="routing-detail-item">
                    <span class="routing-label">Reason</span>
                    <span class="routing-value">${reason}</span>
                </div>
                <div class="routing-detail-item">
                    <span class="routing-label">Query Type</span>
                    <span class="routing-value">${query_metadata.query_type}</span>
                </div>
                <div class="routing-detail-item">
                    <span class="routing-label">Complexity</span>
                    <span class="routing-value">${query_metadata.complexity}</span>
                </div>
            </div>
        `;
    }

    formatMessage(text) {
        // Simple markdown-like formatting
        let formatted = this.escapeHtml(text);

        // Code blocks
        formatted = formatted.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang || 'text'}">${code.trim()}</code></pre>`;
        });

        // Inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Line breaks
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showError(message) {
        this.providerStatus.innerHTML = `
            <div class="error-message">${message}</div>
        `;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new LLMRouterApp();
});

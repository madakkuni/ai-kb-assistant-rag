document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const chatForm = document.getElementById('chatForm');
    const queryInput = document.getElementById('queryInput');
    const chatContainer = document.getElementById('chatContainer');
    const welcomeBox = document.getElementById('welcomeBox');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadStatus = document.getElementById('uploadStatus');
    const evalModeToggle = document.getElementById('evalModeToggle');
    const metricsBtn = document.getElementById('metricsBtn');

    if (localStorage.getItem('theme') === 'dark') {
        body.classList.replace('light-mode', 'dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('light-mode')) {
            body.classList.replace('light-mode', 'dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.replace('dark-mode', 'light-mode');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
        }
    });

    clearChatBtn.addEventListener('click', clearChat);
    newChatBtn.addEventListener('click', clearChat);

    function clearChat() {
        chatContainer.innerHTML = '';
        chatContainer.appendChild(welcomeBox);
        welcomeBox.style.display = 'block';
    }

    document.querySelectorAll('.suggestion-badge').forEach(badge => {
        badge.addEventListener('click', () => {
            queryInput.value = badge.textContent;
            queryInput.focus();
        });
    });

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        uploadStatus.classList.add('d-none');

        try {
            const res = await fetch('/api/upload', { method: 'POST', body: formData });
            if (res.ok) {
                uploadStatus.classList.remove('d-none');
                fileInput.value = '';
            } else {
                alert('Upload failed');
            }
        } catch (err) {
            alert('Upload error');
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = '<i class="fas fa-upload me-1"></i> Upload & Ingest';
            setTimeout(() => uploadStatus.classList.add('d-none'), 3000);
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        queryInput.value = '';
        welcomeBox.style.display = 'none';

        appendMessage('user', query);
        const typingId = appendTypingIndicator();

        const evalMode = evalModeToggle.checked;

        try {
            const res = await fetch(`/api/chat?eval=${evalMode}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            removeTypingIndicator(typingId);

            if (!res.ok) {
                appendMessage('bot', 'Sorry, I encountered an error while processing your request.');
                return;
            }

            const data = await res.json();
            await simulateTyping(data);
            updateHistory();

        } catch (err) {
            removeTypingIndicator(typingId);
            appendMessage('bot', 'Network error or server unreachable.');
        }
    });

    function appendMessage(sender, text, htmlExtras = "") {
        const id = 'msg-' + Date.now();
        const wrapper = document.createElement('div');
        wrapper.className = `message-bubble ${sender}`;
        wrapper.id = id;

        const content = document.createElement('div');
        content.className = 'message-content';
        
        if (sender === 'user') {
            content.textContent = text;
        } else {
            content.innerHTML = text + htmlExtras;
        }

        wrapper.appendChild(content);

        if (sender === 'bot') {
            const actions = document.createElement('div');
            actions.className = 'message-actions';
            
            const copyBtn = document.createElement('button');
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.onclick = () => {
                const pureText = content.textContent;
                navigator.clipboard.writeText(pureText);
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy', 2000);
            };
            
            actions.appendChild(copyBtn);
            wrapper.appendChild(actions);
        }

        chatContainer.appendChild(wrapper);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const wrapper = document.createElement('div');
        wrapper.className = `message-bubble bot`;
        wrapper.id = id;
        const content = document.createElement('div');
        content.className = 'message-content typing-indicator';
        content.innerHTML = '<span></span><span></span><span></span>';
        wrapper.appendChild(content);
        chatContainer.appendChild(wrapper);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    async function simulateTyping(data) {
        let answer = data.answer || "No response generated.";
        let sourcesHtml = '';
        
        if (data.sources && data.sources.length > 0) {
            sourcesHtml += '<div class="mt-3 border-top pt-2"><strong>Sources:</strong><br>';
            data.sources.forEach(src => {
                const link = `/docs/${encodeURIComponent(src.source)}`;
                sourcesHtml += `<a href="${link}" target="_blank" class="source-item" style="text-decoration: none;" title="Chunks: ${src.chunks}"><i class="fas fa-file-alt me-1"></i> ${src.source}</a>`;
            });
            sourcesHtml += '</div>';
        }

        if (data.evaluation) {
            sourcesHtml += `<div class="eval-stats">Eval: F=${data.evaluation.faithfulness.toFixed(2)} | CP=${data.evaluation.context_precision.toFixed(2)} | R=${data.evaluation.answer_relevance.toFixed(2)}</div>`;
        }
        
        const msgId = appendMessage('bot', '', sourcesHtml);
        const msgWrapper = document.getElementById(msgId);
        const contentDiv = msgWrapper.querySelector('.message-content');
        
        let i = 0;
        let speed = 15; 
        
        contentDiv.innerHTML = sourcesHtml;
        
        return new Promise(resolve => {
            function typeWriter() {
                if (i < answer.length) {
                    const currentText = answer.substring(0, i + 1).replace(/\n/g, '<br>');
                    contentDiv.innerHTML = currentText + sourcesHtml;
                    i++;
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                    setTimeout(typeWriter, speed);
                } else {
                    resolve();
                }
            }
            typeWriter();
        });
    }

    async function updateHistory() {
        try {
            const res = await fetch('/api/history');
            if (res.ok) {
                const data = await res.json();
                const hl = document.getElementById('historyList');
                hl.innerHTML = '';
                data.history.reverse().forEach(req => {
                    const el = document.createElement('div');
                    el.className = 'history-item';
                    el.title = req.query;
                    el.innerHTML = `<i class="fas fa-comment fa-sm me-2 text-primary"></i> ${req.query}`;
                    el.onclick = () => {
                        queryInput.value = req.query;
                        queryInput.focus();
                    };
                    hl.appendChild(el);
                });
            }
        } catch(e) {}
    }

    metricsBtn.addEventListener('click', async () => {
        const mb = document.getElementById('metricsBody');
        mb.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        try {
            const res = await fetch('/api/metrics');
            const data = await res.json();
            mb.innerHTML = `
                <table class="table table-sm">
                    <tbody>
                        <tr><th>Total Requests</th><td>${data.total_requests}</td></tr>
                        <tr><th>Total Tokens</th><td>${data.total_tokens}</td></tr>
                        <tr><th>P50 Latency</th><td>${data.p50_latency.toFixed(2)} s</td></tr>
                        <tr><th>P95 Latency</th><td>${data.p95_latency.toFixed(2)} s</td></tr>
                    </tbody>
                </table>
            `;
        } catch(e) {
            mb.innerHTML = 'Error loading metrics.';
        }
    });

    updateHistory();
});

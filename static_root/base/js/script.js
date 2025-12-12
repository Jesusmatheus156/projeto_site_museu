document.addEventListener('DOMContentLoaded', () => {
    // ==============================================
    // 1. LÓGICA DO MENU HAMBURGER
    // ==============================================
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.navigation');

    hamburger.addEventListener('click', () => {
        // Toggle da classe 'active' para mudar o ícone (hamburger <-> X)
        hamburger.classList.toggle('active');
        // Toggle da classe 'active' para mostrar/esconder o menu
        navLinks.classList.toggle('active');
        
        // Acessibilidade: atualiza o estado do menu
        const isExpanded = navLinks.classList.contains('active');
        hamburger.setAttribute('aria-expanded', isExpanded);
    });


    // ==============================================
    // 2. LÓGICA DO PAINEL DE ACESSIBILIDADE UNIFICADO
    // ==============================================
    const btnToggleAcess = document.getElementById('btn-acessibilidade-toggle');
    const panelAcess = document.getElementById('acessibilidade-panel');

    // Toggle do painel
    btnToggleAcess.addEventListener('click', () => {
        const isHidden = panelAcess.getAttribute('aria-hidden') === 'true';
        panelAcess.setAttribute('aria-hidden', !isHidden);
        panelAcess.classList.toggle('active', isHidden);
    });

    // Fechar painel ao clicar fora
    document.addEventListener('click', (e) => {
        if (!panelAcess.contains(e.target) && !btnToggleAcess.contains(e.target) && panelAcess.classList.contains('active')) {
            panelAcess.classList.remove('active');
            panelAcess.setAttribute('aria-hidden', 'true');
        }
    });

    // Toggle de Áudio Descrição
    const btnAudioDesc = document.getElementById('btn-audio-desc-toggle');
    const audioStatus = document.getElementById('audio-desc-status');
    btnAudioDesc.addEventListener('click', () => {
        const isActive = document.body.classList.toggle('audio-active');
        btnAudioDesc.classList.toggle('active', isActive);
        audioStatus.textContent = isActive ? 'Desativar' : 'Ativar';
        
        // Lógica real de Audio Descrição (Texto para Voz) viria aqui:
        if (isActive) {
            console.log("Áudio Descrição Ativada. Começando leitura dos elementos com data-audio-desc.");
            // Ex: Implementar um script que percorre os elementos e lê o texto.
            // A API de Web Speech (SpeechSynthesis) do navegador pode ser usada.
        } else {
            console.log("Áudio Descrição Desativada.");
            // Ex: Parar a leitura.
            if (window.speechSynthesis) window.speechSynthesis.cancel();
        }
    });

    // Lógica de Alto Contraste (Baseada no seu código original)
    document.getElementById("btn-contraste-toggle").onclick = () => {
        document.body.classList.toggle("high-contrast");
        const isContrastActive = document.body.classList.contains("high-contrast");
        localStorage.setItem("contraste", isContrastActive ? "on" : "off");
    };

    // Lógica de Fonte (Baseada no seu código original)
    let fonte = parseFloat(localStorage.getItem("fontSize")) || 1.0;
    document.documentElement.style.fontSize = fonte + "em";

    document.getElementById("btn-font-aumentar").onclick = () => {
        fonte = Math.min(fonte + 0.1, 1.5); // Limite de aumento
        document.documentElement.style.fontSize = fonte + "em";
        localStorage.setItem("fontSize", fonte);
    };

    document.getElementById("btn-font-diminuir").onclick = () => {
        fonte = Math.max(fonte - 0.1, 0.8); // Limite de diminuição
        document.documentElement.style.fontSize = fonte + "em";
        localStorage.setItem("fontSize", fonte);
    };

    document.getElementById("btn-font-reset").onclick = () => {
        fonte = 1.0;
        document.documentElement.style.fontSize = "1em";
        localStorage.setItem("fontSize", fonte);

        document.body.classList.remove("high-contrast");
        localStorage.setItem("contraste", "off");
        
        document.body.classList.remove("audio-active");
        btnAudioDesc.classList.remove('active');
        audioStatus.textContent = 'Ativar';
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    };

    // Aplica o contraste ao carregar se estiver salvo
    if (localStorage.getItem("contraste") === "on") {
        document.body.classList.add("high-contrast");
    }
});
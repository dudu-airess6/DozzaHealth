document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = 'http://127.0.0.1:8000';

    // ============================================================
    // UTILITÁRIOS DE INTERFACE (Toast e Modal Customizado)
    // ============================================================
    function mostrarToast(mensagem, tipo = 'sucesso') {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${tipo}`;
        toast.innerHTML = `<span>${mensagem}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    function confirmarAcao(titulo, mensagem) {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'custom-modal-overlay';
            overlay.innerHTML = `
                <div class="custom-modal-box">
                    <h3>${titulo}</h3>
                    <p>${mensagem}</p>
                    <div class="custom-modal-actions">
                        <button class="btn-secondary" id="btnModalCancelar">Cancelar</button>
                        <button class="btn-primary" id="btnModalConfirmar">Confirmar</button>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);

            const btnConfirmar = overlay.querySelector('#btnModalConfirmar');
            const btnCancelar = overlay.querySelector('#btnModalCancelar');

            btnConfirmar.addEventListener('click', () => {
                overlay.remove();
                resolve(true);
            });

            btnCancelar.addEventListener('click', () => {
                overlay.remove();
                resolve(false);
            });
        });
    }

    // ============================================================
    // 0. NAVEGAÇÃO / NAVBAR (Ativação Automática de Abas)
    // ============================================================
    const linkAtual = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-item');

    navLinks.forEach(link => {
        const hrefLink = link.getAttribute('href');
        if (hrefLink === linkAtual) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // ============================================================
    // 1. TELA DE LOGIN (index.html)
    // ============================================================
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        const btnCadastrar = document.getElementById('btnCadastrar');
        const mensagemFeedback = document.getElementById('mensagemFeedback');

        loginForm.addEventListener('submit', async (evento) => {
            evento.preventDefault();

            const credencial = document.getElementById('credencial').value;
            const senha = document.getElementById('senha').value;

            try {
                const resposta = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ usuario: credencial, senha: senha })
                });

                const dados = await resposta.json();

                if (resposta.ok) {
                    if (dados.access_token) {
                        localStorage.setItem('token', dados.access_token);
                        localStorage.setItem('tipo_usuario', dados.tipo_usuario);
                        localStorage.setItem('nome_usuario', dados.nome);
                    }

                    mensagemFeedback.style.color = '#77dd77';
                    mensagemFeedback.textContent = dados.mensagem || 'Login realizado com sucesso! Redirecionando...';

                    setTimeout(() => {
                        if (dados.tipo_usuario === 'Farmaceutico') {
                            window.location.href = 'busca.html';
                        } else {
                            mensagemFeedback.style.color = '#ef4444';
                            mensagemFeedback.textContent = 'Apenas farmacêuticos têm permissão de acesso.';
                        }
                    }, 1000);

                } else {
                    mensagemFeedback.style.color = '#ef4444';
                    mensagemFeedback.textContent = dados.detail || dados.mensagem || 'Credenciais inválidas.';
                }

            } catch (erro) {
                console.error('Erro na requisição de login:', erro);
                mensagemFeedback.style.color = '#ef4444';
                mensagemFeedback.textContent = 'Erro de conexão. Verifique se o servidor na porta 8001 está ativo.';
            }
        });

        if (btnCadastrar) {
            btnCadastrar.addEventListener('click', () => {
                window.location.href = 'cadastro.html';
            });
        }
    }

    // ============================================================
    // 2. TELA DE CADASTRO (cadastro.html)
    // ============================================================
    const cadastroForm = document.getElementById('cadastroForm');
    if (cadastroForm) {
        const mensagemFeedbackCad = document.getElementById('mensagemFeedback');
        const btnVoltarLogin = document.getElementById('btnVoltarLogin');

        cadastroForm.addEventListener('submit', async (evento) => {
            evento.preventDefault();

            const nome = document.getElementById('nome').value;
            const login = document.getElementById('login').value;
            const senha = document.getElementById('senha').value;
            const tipo_usuario = document.getElementById('tipo_usuario').value;
            const crf = document.getElementById('crf') ? document.getElementById('crf').value : null;

            try {
                const resposta = await fetch(`${API_BASE}/auth/cadastro`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome, login, senha, tipo_usuario, crf })
                });

                const dados = await resposta.json();

                if (resposta.ok) {
                    mensagemFeedbackCad.style.color = '#77dd77';
                    mensagemFeedbackCad.textContent = 'Usuário cadastrado com sucesso! Redirecionando para login...';
                    setTimeout(() => { window.location.href = 'index.html'; }, 1500);
                } else {
                    mensagemFeedbackCad.style.color = '#ef4444';
                    mensagemFeedbackCad.textContent = dados.detail || 'Erro ao realizar cadastro.';
                }
            } catch (erro) {
                console.error('Erro na requisição de cadastro:', erro);
                mensagemFeedbackCad.style.color = '#ef4444';
                mensagemFeedbackCad.textContent = 'Erro de conexão com o servidor.';
            }
        });

        if (btnVoltarLogin) {
            btnVoltarLogin.addEventListener('click', () => {
                window.location.href = 'index.html';
            });
        }
    }

    // ============================================================
    // 3. TELA DE BUSCA / DASHBOARD (busca.html)
    // ============================================================
    const formBusca = document.getElementById('formBusca');
    if (formBusca) {
        const token = localStorage.getItem('token');
        const tipoUsuario = localStorage.getItem('tipo_usuario');
        const nomeUsuario = localStorage.getItem('nome_usuario');

        if (!token || tipoUsuario !== 'Farmaceutico') {
            mostrarToast('Acesso negado. Faça login como Farmacêutico.', 'erro');
            localStorage.clear();
            setTimeout(() => { window.location.href = 'index.html'; }, 1500);
            return;
        }

        const labelUsuario = document.getElementById('labelUsuario');
        if (labelUsuario) {
            labelUsuario.textContent = `Farm. ${nomeUsuario || 'Usuário'}`;
        }

        const inputQuery = document.getElementById('inputQuery');
        const gridResultados = document.getElementById('gridResultados');
        const infoTotal = document.getElementById('infoTotal');
        const paginacao = document.getElementById('paginacao');
        const btnLogout = document.getElementById('btnLogout');
        const filterChips = document.getElementById('filterChips');
        const btnLimparFiltros = document.getElementById('btnLimparFiltros');

        let paginaAtual = 1;
        const limitePorPagina = 12;
        let totalRegistrosAtual = 0;

        // Captura formas ativas selecionadas nos chips
        function obterFormasSelecionadas() {
            if (!filterChips) return [];
            const chipsAtivos = filterChips.querySelectorAll('.chip-btn[data-value].active');
            return Array.from(chipsAtivos)
                .map(c => c.getAttribute('data-value'))
                .filter(Boolean);
        }

        // Debounce na digitação (400ms)
        let timerDebounce = null;
        if (inputQuery) {
            inputQuery.addEventListener('input', () => {
                clearTimeout(timerDebounce);
                timerDebounce = setTimeout(() => {
                    paginaAtual = 1;
                    executarBusca();
                }, 400);
            });
        }

        // Múltipla seleção nos chips
        if (filterChips) {
            const chipTodas = filterChips.querySelector('.chip-btn[data-value=""]');
            const chipsEspecificos = filterChips.querySelectorAll('.chip-btn[data-value]:not([data-value=""])');

            if (chipTodas) {
                chipTodas.addEventListener('click', () => {
                    chipsEspecificos.forEach(c => c.classList.remove('active'));
                    chipTodas.classList.add('active');
                    paginaAtual = 1;
                    executarBusca();
                });
            }

            chipsEspecificos.forEach(chip => {
                chip.addEventListener('click', () => {
                    chip.classList.toggle('active');

                    const temAlgumSelecionado = Array.from(chipsEspecificos).some(c => c.classList.contains('active'));

                    if (temAlgumSelecionado) {
                        if (chipTodas) chipTodas.classList.remove('active');
                    } else {
                        if (chipTodas) chipTodas.classList.add('active');
                    }

                    paginaAtual = 1;
                    executarBusca();
                });
            });
        }

        // Botão Limpar Filtros
        if (btnLimparFiltros) {
            btnLimparFiltros.addEventListener('click', () => {
                if (inputQuery) inputQuery.value = '';

                if (filterChips) {
                    const chips = filterChips.querySelectorAll('.chip-btn[data-value]');
                    chips.forEach(c => c.classList.remove('active'));
                    const chipTodas = filterChips.querySelector('.chip-btn[data-value=""]');
                    if (chipTodas) chipTodas.classList.add('active');
                }

                paginaAtual = 1;
                executarBusca();
                mostrarToast('Filtros e busca resetados.', 'info');
            });
        }

        if (btnLogout) {
            btnLogout.addEventListener('click', () => {
                localStorage.clear();
                window.location.href = 'index.html';
            });
        }

        formBusca.addEventListener('submit', (e) => {
            e.preventDefault();
            paginaAtual = 1;
            executarBusca();
        });

        async function executarBusca() {
            const query = inputQuery ? inputQuery.value.trim() : '';
            const formasSelecionadas = obterFormasSelecionadas();

            const params = new URLSearchParams({
                page: paginaAtual,
                limit: limitePorPagina
            });

            if (query) params.append('q', query);

            // Envia filtros múltiplos unidos por vírgula (?forma=Gotas,Xarope)
            if (formasSelecionadas.length > 0) {
                params.append('forma', formasSelecionadas.join(','));
            }

            gridResultados.innerHTML = '<p>Buscando medicamentos...</p>';
            if (infoTotal) infoTotal.textContent = 'Atualizando estoque...';

            try {
                const resposta = await fetch(`${API_BASE}/api/v1/buscar?${params.toString()}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json'
                    }
                });

                if (resposta.status === 401 || resposta.status === 403) {
                    mostrarToast('Sessão expirada. Faça login novamente.', 'erro');
                    localStorage.clear();
                    setTimeout(() => { window.location.href = 'index.html'; }, 1500);
                    return;
                }

                if (!resposta.ok) {
                    throw new Error('Erro na consulta');
                }

                const dados = await resposta.json();
                renderizarResultados(dados);

            } catch (erro) {
                console.error('Erro na busca:', erro);
                gridResultados.innerHTML = '<p style="color: red;">Erro ao carregar medicamentos. Verifique se o backend está rodando.</p>';
                if (infoTotal) infoTotal.textContent = 'Total de registros em estoque: --';
            }
        }

        function renderizarResultados(dados) {
            const { total_encontrados, resultados } = dados;

            const historicoFracionados = JSON.parse(localStorage.getItem('medicamentos_fracionados') || '[]');
            const idsFracionados = historicoFracionados
                .map(item => (item && item.id !== undefined && item.id !== null) ? String(item.id) : null)
                .filter(Boolean);

            const resultadosFiltrados = (resultados || []).filter(med => {
                const medId = med.id || med.id_medicamento;
                return medId !== undefined && medId !== null ? !idsFracionados.includes(String(medId)) : true;
            });

            totalRegistrosAtual = Math.max(0, (total_encontrados || 0) - idsFracionados.length);

            if (infoTotal) {
                infoTotal.textContent = `Total de registros em estoque: ${totalRegistrosAtual}`;
            }

            gridResultados.innerHTML = '';

            if (resultadosFiltrados.length === 0) {
                gridResultados.innerHTML = '<p>Nenhum medicamento encontrado para os filtros selecionados.</p>';
                if (paginacao) paginacao.classList.add('hidden');
                return;
            }

            resultadosFiltrados.forEach(med => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div>
                        <h3>${med.nome_comercial || med.nome || 'N/A'}</h3>
                        <p><strong>Princípio Ativo:</strong> ${med.principio_ativo || 'N/A'}</p>
                        <p><strong>Concentração:</strong> ${med.concentracao || 'N/A'}</p>
                        <p><strong>Instruções:</strong> ${med.instrucoes_prescricao || 'N/A'}</p>
                        <span class="tag-forma">${med.forma_farmaceutica || 'Líquido'}</span>
                    </div>
                    <button class="btn-fracionar">
                        ⚙️ Fracionar Medicamento
                    </button>
                `;

                const btnFracionar = card.querySelector('.btn-fracionar');
                btnFracionar.addEventListener('click', () => {
                    fracionarMedicamentoLocal(med, card);
                });

                gridResultados.appendChild(card);
            });

            const totalPaginas = Math.ceil(totalRegistrosAtual / limitePorPagina);
            if (paginacao) {
                renderizarControlesPaginacao(totalPaginas, paginaAtual, paginacao, (novaPagina) => {
                    paginaAtual = novaPagina;
                    executarBusca();
                });
            }
        }

        function renderizarControlesPaginacao(totalPaginas, paginaAtual, container, aoMudarPagina) {
            container.innerHTML = '';

            if (totalPaginas <= 1) {
                container.classList.add('hidden');
                return;
            }
            container.classList.remove('hidden');

            const btnAnterior = document.createElement('button');
            btnAnterior.textContent = '« Anterior';
            btnAnterior.disabled = (paginaAtual === 1);
            btnAnterior.addEventListener('click', () => aoMudarPagina(paginaAtual - 1));
            container.appendChild(btnAnterior);

            let paginas = [];

            if (totalPaginas <= 6) {
                for (let i = 1; i <= totalPaginas; i++) paginas.push(i);
            } else {
                paginas.push(1);

                let inicio = Math.max(2, paginaAtual);
                let fim = Math.min(totalPaginas - 1, paginaAtual + 2);

                if (paginaAtual === 1) {
                    fim = Math.min(totalPaginas - 1, 3);
                }

                if (inicio > 2) {
                    paginas.push('...');
                }

                for (let i = inicio; i <= fim; i++) {
                    if (!paginas.includes(i)) paginas.push(i);
                }

                if (fim < totalPaginas - 1) {
                    paginas.push('...');
                }

                if (!paginas.includes(totalPaginas)) {
                    paginas.push(totalPaginas);
                }
            }

            paginas.forEach(p => {
                if (p === '...') {
                    const span = document.createElement('span');
                    span.textContent = '...';
                    span.className = 'pagination-ellipsis';
                    container.appendChild(span);
                } else {
                    const btnPage = document.createElement('button');
                    btnPage.textContent = p;
                    if (p === paginaAtual) {
                        btnPage.classList.add('active');
                    } else {
                        btnPage.addEventListener('click', () => aoMudarPagina(p));
                    }
                    container.appendChild(btnPage);
                }
            });

            const btnProxima = document.createElement('button');
            btnProxima.textContent = 'Próxima »';
            btnProxima.disabled = (paginaAtual === totalPaginas);
            btnProxima.addEventListener('click', () => aoMudarPagina(paginaAtual + 1));
            container.appendChild(btnProxima);
        }

        async function fracionarMedicamentoLocal(med, cardElement) {
            const nomeMed = med.nome_comercial || med.nome || 'Medicamento';
            const medId = med.id || med.id_medicamento || Date.now();

            const confirmou = await confirmarAcao(
                '⚙️ Confirmar Fracionamento',
                `Deseja fracionar o medicamento "${nomeMed}"?\n\nEle será removido do estoque visual e registrado no histórico de Fracionados.`
            );

            if (!confirmou) return;

            const historicoFracionados = JSON.parse(localStorage.getItem('medicamentos_fracionados') || '[]');

            const novoRegistro = {
                id: String(medId),
                nome_medicamento: nomeMed,
                principio_ativo: med.principio_ativo || 'N/A',
                data_hora: new Date().toLocaleString('pt-BR'),
                responsavel: localStorage.getItem('nome_usuario') || 'Usuário'
            };

            historicoFracionados.push(novoRegistro);
            localStorage.setItem('medicamentos_fracionados', JSON.stringify(historicoFracionados));

            cardElement.style.transition = 'all 0.4s ease';
            cardElement.style.opacity = '0';
            cardElement.style.transform = 'scale(0.8)';

            setTimeout(() => {
                cardElement.remove();

                if (totalRegistrosAtual > 0) {
                    totalRegistrosAtual--;
                    if (infoTotal) {
                        infoTotal.textContent = `Total de registros em estoque: ${totalRegistrosAtual}`;
                    }
                }

                if (gridResultados.children.length === 0) {
                    gridResultados.innerHTML = '<p>Nenhum medicamento restante nesta página.</p>';
                }

            }, 400);

            mostrarToast(`Medicamento "${nomeMed}" movido para Fracionados com sucesso!`, 'sucesso');
        }

        executarBusca();
    }

    // ============================================================
    // 4. TELA DE MEDICAMENTOS FRACIONADOS (fracionados.html)
    // ============================================================
    const tabelaFracionadosBody = document.getElementById('tabelaFracionadosBody');
    if (tabelaFracionadosBody) {
        const nomeUsuario = localStorage.getItem('nome_usuario');

        const labelUsuario = document.getElementById('labelUsuario');
        if (labelUsuario) {
            labelUsuario.textContent = `Farm. ${nomeUsuario || 'Usuário'}`;
        }

        const btnLogout = document.getElementById('btnLogout');
        if (btnLogout) {
            btnLogout.addEventListener('click', () => {
                localStorage.clear();
                window.location.href = 'index.html';
            });
        }

        function carregarFracionadosLocais() {
            const dados = JSON.parse(localStorage.getItem('medicamentos_fracionados') || '[]');
            tabelaFracionadosBody.innerHTML = '';

            if (!dados || dados.length === 0) {
                tabelaFracionadosBody.innerHTML = `
                    <tr>
                        <td colspan="5" style="padding: 20px; text-align: center; color: #888;">
                            Nenhum medicamento fracionado registrado até o momento.
                        </td>
                    </tr>`;
                return;
            }

            dados.forEach(item => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid #e5e7eb';
                tr.innerHTML = `
                    <td style="padding: 14px 16px; font-weight: 600; color: #4a4a4a;">${item.nome_medicamento || 'N/A'}</td>
                    <td style="padding: 14px 16px; color: #6b7280;">${item.principio_ativo || 'N/A'}</td>
                    <td style="padding: 14px 16px; color: #6b7280;">${item.data_hora}</td>
                    <td style="padding: 14px 16px; color: #4a4a4a; font-weight: 500;">Farm. ${item.responsavel}</td>
                    <td style="padding: 14px 16px; text-align: center;">
                        <button class="btn-primary btn-relatorio-single" style="padding: 6px 12px; font-size: 12px;">
                            📋 Ver Relatório
                        </button>
                    </td>
                `;

                const btnRelatorio = tr.querySelector('.btn-relatorio-single');
                btnRelatorio.addEventListener('click', () => {
                    gerarRelatorioIndividual(item);
                });

                tabelaFracionadosBody.appendChild(tr);
            });
        }

        function gerarRelatorioIndividual(item) {
            const janelaImpressao = window.open('', '_blank');

            janelaImpressao.document.write(`
                <!DOCTYPE html>
                <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <title>Relatório de Fracionamento - ${item.nome_medicamento}</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 40px; color: #333; line-height: 1.6; }
                        .header { border-bottom: 2px solid #278527; padding-bottom: 10px; margin-bottom: 20px; }
                        .header h1 { color: #278527; margin: 0; font-size: 22px; }
                        .box { background: #f9fafb; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top: 20px; }
                        .box p { margin: 8px 0; }
                        .btn-print { margin-top: 25px; padding: 10px 20px; background-color: #278527; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
                        @media print { .btn-print { display: none; } }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>DozzaHealth — Relatório de Fracionamento</h1>
                    </div>
                    <div class="box">
                        <p><strong>Medicamento:</strong> ${item.nome_medicamento}</p>
                        <p><strong>Princípio Ativo:</strong> ${item.principio_ativo}</p>
                        <p><strong>Data e Hora do Processo:</strong> ${item.data_hora}</p>
                        <p><strong>Responsável Operacional:</strong> Farm. ${item.responsavel}</p>
                        <p><strong>Status do Registro:</strong> Fracionado / Liberado para Dispensação</p>
                    </div>
                    <button class="btn-print" onclick="window.print()">🖨️ Imprimir Relatório</button>
                </body>
                </html>
            `);
            janelaImpressao.document.close();
        }

        const btnImprimirGeral = document.getElementById('btnImprimirRelatorioGeral');
        if (btnImprimirGeral) {
            btnImprimirGeral.addEventListener('click', () => window.print());
        }

        carregarFracionadosLocais();
    }
});
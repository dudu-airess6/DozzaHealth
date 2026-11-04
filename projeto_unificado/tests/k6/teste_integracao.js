import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    teste_integracao: {
      executor: 'per-vu-iterations',
      vus: 1,
      iterations: 1, // Executa o fluxo completo 1 vez para validação funcional
    },
  },
  thresholds: {
    checks: ['rate==1.0'], // Exige 100% de aprovação nos testes funcionais
  },
};

const BASE_URL = 'http://127.0.0.1:8000/api';

export default function () {
  // Gera credenciais únicas por execução para não colidir com dados existentes
  const timestamp = Date.now();
  const usuarioDinamico = {
    nome: 'Doutor Integracao',
    login: `medico_${timestamp}`,
    senha: 'SenhaSegura123!',
    tipo_usuario: 'Medico',
    crm: `CRM-${timestamp.toString().slice(-6)}`,
    especialidade: 'Cardiologia',
  };

  // PASSO 1: Cadastrar novo usuário (POST /api/cadastro)
  const resCadastro = http.post(
    `${BASE_URL}/cadastro`,
    JSON.stringify(usuarioDinamico),
    { headers: { 'Content-Type': 'application/json' } }
  );

  const cadastroSucesso = check(resCadastro, {
    '[Passo 1] Cadastro efetuado com Status 201': (r) => r.status === 201,
    '[Passo 1] Retornou id do usuario': (r) => {
      const body = JSON.parse(r.body);
      return body.usuario_id !== undefined;
    },
  });

  sleep(1);

  // PASSO 2: Fazer login com o usuário recém-criado (POST /api/login)
  if (cadastroSucesso) {
    const resLogin = http.post(
      `${BASE_URL}/login`,
      JSON.stringify({
        usuario: usuarioDinamico.login,
        senha: usuarioDinamico.senha,
      }),
      { headers: { 'Content-Type': 'application/json' } }
    );

    check(resLogin, {
      '[Passo 2] Login efetuado com Status 200': (r) => r.status === 200,
      '[Passo 2] Retornou tipo de usuario correto': (r) => {
        const body = JSON.parse(r.body);
        return body.tipo_usuario === 'Medico';
      },
    });
  }

  sleep(1);

  // PASSO 3: Tentar cadastrar o mesmo login para validar regra de duplicidade
  const resDuplicado = http.post(
    `${BASE_URL}/cadastro`,
    JSON.stringify(usuarioDinamico),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(resDuplicado, {
    '[Passo 3] Bloqueio de duplicidade com Status 400': (r) => r.status === 400,
    '[Passo 3] Mensagem de erro de login em uso': (r) => {
      const body = JSON.parse(r.body);
      return body.detail === 'Este login já está em uso.';
    },
  });
}
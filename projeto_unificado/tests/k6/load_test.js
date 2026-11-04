import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 20 }, // Rampa de subida para 20 usuários em 10s
    { duration: '30s', target: 50 }, // Mantém a carga em 50 usuários por 30s
    { duration: '10s', target: 0 },  // Rampa de descida para 0 em 10s
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],   // Taxa de erros abaixo de 1%
    http_req_duration: ['p(95)<500'], // 95% das requisições abaixo de 500ms
  },
};

export default function () {
  const url = 'http://127.0.0.1:8000/auth/login';
  
  // O schema da API exige as chaves "usuario" e "senha"
  const payload = JSON.stringify({
    usuario: 'testuser',
    senha: 'secretpassword',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  if (res.status !== 200) {
    console.log(`Erro Status: ${res.status} | Resposta: ${res.body}`);
  }

  check(res, {
    'status e 200': (r) => r.status === 200,
    'tempo de resposta aceitavel': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
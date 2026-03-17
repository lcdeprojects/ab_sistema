# Projeto: AB Advocacia - Gestão Jurídica Inteligente

Sistema robusto para gestão de clientes, processos judiciais, controle de atividades e financeiro, construído com Django para máxima segurança e produtividade.

## User Review Required

> [!IMPORTANT]
> **Armazenamento Local:** Como os arquivos serão salvos localmente no Docker, é fundamental garantir volumes persistentes para não perder dados ao reiniciar o container.
> **Segurança:** Implementaremos autenticação baseada em Django com permissões específicas para que advogados vejam apenas seus processos atribuídos.

## Proposed Changes

### 🛠️ Core & Infrastructure
- **Django 5.0:** Framework principal.
- **PostgreSQL:** Banco de dados relacional robusto.
- **Docker & Docker Compose:** Containerização completa para deploy facilitado.
- **Tailwind CSS:** Para interface moderna e responsiva (Dark/Light Mode).

---

### 💾 Database Schema (Principais Modelos)

#### [NEW] `models.py`
- **User (Custom):** Extensão do Django User para perfis de advogados/colaboradores.
- **Cliente:** (Nome, CPF, Telefone, WhatsApp, E-mail).
- **Processo:** (Número, Título, Cliente (FK), Advogado Responsável (FK), Status (Enum), Descrição).
- **Atividade/Histórico:** (Processo (FK), Advogado (FK), Comentário, Data/Hora, Arquivo Anexo).
- **Transação Financeira:** (Cliente (FK), Tipo (Entrada), Valor, Data, Descrição, Status de Pagamento).

---

### 🎨 Frontend & UI
- **Dashboard:** Visão geral com métricas (count de processos por advogado).
- **Kanban:** Interface visual para status de processos usando Tailwind + Drag'n'Drop simples.
- **Theme Switcher:** Ativação dinâmica entre modo claro e escuro.

---

### 📂 File Structure (Project Root: `./`)
- `manage.py`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `core/` (Configurações do Django)
- `apps/`
    - `users/`
    - `clientes/`
    - `processos/`
    - `financeiro/`
- `static/` (Tailwind output, JS, Imagens)
- `templates/` (Base, Layouts, Components)
- `media/` (Local storage para documentos)

---

## Task Breakdown

### Phase 1: Foundation (Infra & Config)
1. **Setup Project:** Inicializar Django, Dockerfile e docker-compose.
   - **Agent:** `backend-specialist` | **Skill:** `python-patterns`
   - **INPUT:** Requisitos de deploy | **OUTPUT:** `docker-compose up` rodando Django + Postgres | **VERIFY:** Acesso ao localhost:8000.
2. **Setup Tailwind & Base UI:** Integrar Tailwind e criar `base.html`.
   - **Agent:** `frontend-specialist` | **Skill:** `tailwind-patterns`
   - **INPUT:** Design Guidelines | **OUTPUT:** Template base com Dark Mode | **VERIFY:** CSS compilando corretamente.

### Phase 2: CRM & Processos
3. **Clientes CRUD:** Telas de cadastro/lista de clientes.
   - **Agent:** `backend-specialist` | **Skill:** `clean-code`
   - **INPUT:** Campos de cliente | **OUTPUT:** Views/Forms de cliente | **VERIFY:** Cadastrar cliente no banco.
4. **Processos & Kanban:** Registro de processos e dashboard kanban.
   - **Agent:** `backend-specialist` | **Skill:** `database-design`
   - **INPUT:** Fluxo de processos | **OUTPUT:** Dashboard kanban filtrável | **VERIFY:** Mudar status e refletir no kanban.

### Phase 3: Histórico & Financeiro
5. **Histórico Detalhado:** Timeline de atualizações com anexo de arquivos.
   - **Agent:** `backend-specialist` | **Skill:** `api-patterns` (Django views)
   - **INPUT:** Requisito de log | **OUTPUT:** Timeline responsiva | **VERIFY:** Upload de arquivo salvo em `/media`.
6. **Controle Financeiro & Export:** Lançamentos e exportação Excel (openpyxl).
   - **Agent:** `backend-specialist` | **Skill:** `clean-code`
   - **INPUT:** Dados financeiros | **OUTPUT:** Tela de lançamentos + Botão "Exportar Excel" | **VERIFY:** Gerar arquivo .xlsx válido.

---

## Verification Plan

### Automated Tests
- `python manage.py test`: Rodar suíte de testes unitários para models de Cliente e Processo.
- `python .agent/scripts/checklist.py .`: Verificação de segurança e linting.

### Manual Verification
1. Login como administrador.
2. Criar Cliente -> Atribuir Processo -> Adicionar Atualização com Arquivo.
3. Arrastar processo no Kanban para mudar status.
4. Registrar transação financeira e exportar para Excel.
5. Alternar entre modos Dark e Light.

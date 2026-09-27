# Agent Skills

### A comprehensive, production-grade **skill catalog** for AI coding agents.

[![Skills](https://img.shields.io/badge/Skills-350-8B5CF6?style=for-the-badge)](#skill-catalog)
[![Categories](https://img.shields.io/badge/Categories-10-F59E0B?style=for-the-badge)](#skill-catalog)
[![Compatible Agents](https://img.shields.io/badge/Compatible_Agents-40+-10B981?style=for-the-badge)](#compatible-agents)
[![Specification](https://img.shields.io/badge/Spec-agentskills.io-3B82F6?style=for-the-badge)](https://agentskills.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-EAB308?style=for-the-badge)](LICENSE)
[![Code Style: Prettier](https://img.shields.io/badge/Code_Style-Prettier-EC4899?style=for-the-badge&logo=prettier&logoColor=white)](https://prettier.io)

---

## Installation

Install the entire catalog:

```bash
npx skills add g1joshi/agent-skills/skills
```

Or install specific skills on demand:

```bash
npx skills add g1joshi/agent-skills/skills --skill dart
npx skills add g1joshi/agent-skills/skills --skill flutter
```

---

## Compatible Agents

Compatible with all agents adhering to the `agentskills.io` standard:

![Adal](https://img.shields.io/badge/Adal-6366F1?style=for-the-badge&logoColor=white)
![Amp](https://img.shields.io/badge/Amp-0066FF?style=for-the-badge&logoColor=white)
![Antigravity](https://img.shields.io/badge/Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Augment](https://img.shields.io/badge/Augment-7C3AED?style=for-the-badge&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-D4A27F?style=for-the-badge&logo=anthropic&logoColor=white)
![Cline](https://img.shields.io/badge/Cline-5A67D8?style=for-the-badge&logoColor=white)
![CodeBuddy](https://img.shields.io/badge/CodeBuddy-10B981?style=for-the-badge&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-412991?style=for-the-badge&logo=openai&logoColor=white)
![Command Code](https://img.shields.io/badge/Command_Code-1E3A8A?style=for-the-badge&logoColor=white)
![Continue](https://img.shields.io/badge/Continue-000000?style=for-the-badge&logoColor=white)
![Crush](https://img.shields.io/badge/Crush-EC4899?style=for-the-badge&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)
![Droid](https://img.shields.io/badge/Droid-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white)
![Goose](https://img.shields.io/badge/Goose-FF9900?style=for-the-badge&logoColor=white)
![iFlow CLI](https://img.shields.io/badge/iFlow_CLI-3B82F6?style=for-the-badge&logoColor=white)
![Junie](https://img.shields.io/badge/Junie-000000?style=for-the-badge&logo=jetbrains&logoColor=white)
![Kilo](https://img.shields.io/badge/Kilo-00D4AA?style=for-the-badge&logoColor=white)
![Kimi CLI](https://img.shields.io/badge/Kimi_CLI-000000?style=for-the-badge&logoColor=white)
![Kiro CLI](https://img.shields.io/badge/Kiro_CLI-FF9900?style=for-the-badge&logo=amazon&logoColor=white)
![Kode](https://img.shields.io/badge/Kode-6366F1?style=for-the-badge&logoColor=white)
![MCPJam](https://img.shields.io/badge/MCPJam-F59E0B?style=for-the-badge&logoColor=white)
![Mistral Vibe](https://img.shields.io/badge/Mistral_Vibe-FF7000?style=for-the-badge&logoColor=white)
![Mux](https://img.shields.io/badge/Mux-FA4616?style=for-the-badge&logoColor=white)
![Neovate](https://img.shields.io/badge/Neovate-57A143?style=for-the-badge&logo=neovim&logoColor=white)
![OpenClaw](https://img.shields.io/badge/OpenClaw-6366F1?style=for-the-badge&logoColor=white)
![OpenCode](https://img.shields.io/badge/OpenCode-3B82F6?style=for-the-badge&logoColor=white)
![OpenHands](https://img.shields.io/badge/OpenHands-10B981?style=for-the-badge&logoColor=white)
![Pi](https://img.shields.io/badge/Pi-FF6B6B?style=for-the-badge&logoColor=white)
![Pochi](https://img.shields.io/badge/Pochi-F472B6?style=for-the-badge&logoColor=white)
![Qoder](https://img.shields.io/badge/Qoder-8B5CF6?style=for-the-badge&logoColor=white)
![Qwen Code](https://img.shields.io/badge/Qwen_Code-6366F1?style=for-the-badge&logoColor=white)
![Replit](https://img.shields.io/badge/Replit-F26207?style=for-the-badge&logo=replit&logoColor=white)
![Roo](https://img.shields.io/badge/Roo-E11D48?style=for-the-badge&logoColor=white)
![Trae](https://img.shields.io/badge/Trae-00D6C6?style=for-the-badge&logoColor=white)
![Trae CN](https://img.shields.io/badge/Trae_CN-00D6C6?style=for-the-badge&logoColor=white)
![Windsurf](https://img.shields.io/badge/Windsurf-09B6A2?style=for-the-badge&logo=codeium&logoColor=white)
![Zencoder](https://img.shields.io/badge/Zencoder-14B8A6?style=for-the-badge&logoColor=white)

---

## Skill Catalog

| Category                              | Skills  | Focus Areas                                                            |
| :------------------------------------ | :-----: | :--------------------------------------------------------------------- |
| [`ai-ml`](skills/ai-ml)               |   45    | ML frameworks, LLMs, Vector DBs, Agents, NLP, Data Science             |
| [`architecture`](skills/architecture) |   20    | System design, Microservices, CQRS, Event-Driven, Distributed Systems  |
| [`databases`](skills/databases)       |   30    | Relational, NoSQL, NewSQL, Graph, Vector, Timeseries, ORMs             |
| [`devops`](skills/devops)             |   50    | Containers, Orchestration, CI/CD, IaC, Cloud Providers, Observability  |
| [`frameworks`](skills/frameworks)     |   47    | Modern frontend, backend, fullstack, SSR/SSG, UI component systems     |
| [`languages`](skills/languages)       |   41    | Compiled, interpreted, systems, functional, scripting, shell languages |
| [`mobile`](skills/mobile)             |   13    | iOS, Android, cross-platform runtimes, hybrid frameworks, native SDKs  |
| [`security`](skills/security)         |   19    | Authentication, authorization, encryption, scanning, secret management |
| [`testing`](skills/testing)           |   25    | Unit, E2E, load testing, mocks, component testing, browser automation  |
| [`tools`](skills/tools)               |   60    | IDEs, editors, bundlers, CLIs, terminal tools, linters, debuggers      |
| **Total**                             | **350** | **Comprehensive Production-Ready Skill Catalog**                       |

### AI & Machine Learning (`skills/ai-ml`) — 45 Skills

[![airflow](https://img.shields.io/badge/airflow-8B5CF6?style=flat-square)](skills/ai-ml/airflow) [![catboost](https://img.shields.io/badge/catboost-8B5CF6?style=flat-square)](skills/ai-ml/catboost) [![claude](https://img.shields.io/badge/claude-8B5CF6?style=flat-square)](skills/ai-ml/claude) [![comfyui](https://img.shields.io/badge/comfyui-8B5CF6?style=flat-square)](skills/ai-ml/comfyui) [![cursor-ai](https://img.shields.io/badge/cursor--ai-8B5CF6?style=flat-square)](skills/ai-ml/cursor-ai) [![dalle](https://img.shields.io/badge/dalle-8B5CF6?style=flat-square)](skills/ai-ml/dalle) [![dask](https://img.shields.io/badge/dask-8B5CF6?style=flat-square)](skills/ai-ml/dask) [![dbt](https://img.shields.io/badge/dbt-8B5CF6?style=flat-square)](skills/ai-ml/dbt) [![deepseek](https://img.shields.io/badge/deepseek-8B5CF6?style=flat-square)](skills/ai-ml/deepseek) [![fastai](https://img.shields.io/badge/fastai-8B5CF6?style=flat-square)](skills/ai-ml/fastai) [![gemini](https://img.shields.io/badge/gemini-8B5CF6?style=flat-square)](skills/ai-ml/gemini) [![github-copilot](https://img.shields.io/badge/github--copilot-8B5CF6?style=flat-square)](skills/ai-ml/github-copilot) [![huggingface](https://img.shields.io/badge/huggingface-8B5CF6?style=flat-square)](skills/ai-ml/huggingface) [![jax](https://img.shields.io/badge/jax-8B5CF6?style=flat-square)](skills/ai-ml/jax) [![jupyter](https://img.shields.io/badge/jupyter-8B5CF6?style=flat-square)](skills/ai-ml/jupyter) [![keras](https://img.shields.io/badge/keras-8B5CF6?style=flat-square)](skills/ai-ml/keras) [![langchain](https://img.shields.io/badge/langchain-8B5CF6?style=flat-square)](skills/ai-ml/langchain) [![lightgbm](https://img.shields.io/badge/lightgbm-8B5CF6?style=flat-square)](skills/ai-ml/lightgbm) [![llama](https://img.shields.io/badge/llama-8B5CF6?style=flat-square)](skills/ai-ml/llama) [![llamaindex](https://img.shields.io/badge/llamaindex-8B5CF6?style=flat-square)](skills/ai-ml/llamaindex) [![matplotlib](https://img.shields.io/badge/matplotlib-8B5CF6?style=flat-square)](skills/ai-ml/matplotlib) [![midjourney](https://img.shields.io/badge/midjourney-8B5CF6?style=flat-square)](skills/ai-ml/midjourney) [![mistral](https://img.shields.io/badge/mistral-8B5CF6?style=flat-square)](skills/ai-ml/mistral) [![mlflow](https://img.shields.io/badge/mlflow-8B5CF6?style=flat-square)](skills/ai-ml/mlflow) [![nltk](https://img.shields.io/badge/nltk-8B5CF6?style=flat-square)](skills/ai-ml/nltk) [![numpy](https://img.shields.io/badge/numpy-8B5CF6?style=flat-square)](skills/ai-ml/numpy) [![ollama](https://img.shields.io/badge/ollama-8B5CF6?style=flat-square)](skills/ai-ml/ollama) [![openai-gpt](https://img.shields.io/badge/openai--gpt-8B5CF6?style=flat-square)](skills/ai-ml/openai-gpt) [![opencv](https://img.shields.io/badge/opencv-8B5CF6?style=flat-square)](skills/ai-ml/opencv) [![pandas](https://img.shields.io/badge/pandas-8B5CF6?style=flat-square)](skills/ai-ml/pandas) [![perplexity](https://img.shields.io/badge/perplexity-8B5CF6?style=flat-square)](skills/ai-ml/perplexity) [![plotly](https://img.shields.io/badge/plotly-8B5CF6?style=flat-square)](skills/ai-ml/plotly) [![polars](https://img.shields.io/badge/polars-8B5CF6?style=flat-square)](skills/ai-ml/polars) [![pytorch](https://img.shields.io/badge/pytorch-8B5CF6?style=flat-square)](skills/ai-ml/pytorch) [![ray](https://img.shields.io/badge/ray-8B5CF6?style=flat-square)](skills/ai-ml/ray) [![scikit-learn](https://img.shields.io/badge/scikit--learn-8B5CF6?style=flat-square)](skills/ai-ml/scikit-learn) [![seaborn](https://img.shields.io/badge/seaborn-8B5CF6?style=flat-square)](skills/ai-ml/seaborn) [![spacy](https://img.shields.io/badge/spacy-8B5CF6?style=flat-square)](skills/ai-ml/spacy) [![spark](https://img.shields.io/badge/spark-8B5CF6?style=flat-square)](skills/ai-ml/spark) [![stable-diffusion](https://img.shields.io/badge/stable--diffusion-8B5CF6?style=flat-square)](skills/ai-ml/stable-diffusion) [![tensorflow](https://img.shields.io/badge/tensorflow-8B5CF6?style=flat-square)](skills/ai-ml/tensorflow) [![vaex](https://img.shields.io/badge/vaex-8B5CF6?style=flat-square)](skills/ai-ml/vaex) [![weights-biases](https://img.shields.io/badge/weights--biases-8B5CF6?style=flat-square)](skills/ai-ml/weights-biases) [![whisper](https://img.shields.io/badge/whisper-8B5CF6?style=flat-square)](skills/ai-ml/whisper) [![xgboost](https://img.shields.io/badge/xgboost-8B5CF6?style=flat-square)](skills/ai-ml/xgboost)

### System Architecture (`skills/architecture`) — 20 Skills

[![api-gateway](https://img.shields.io/badge/api--gateway-10B981?style=flat-square)](skills/architecture/api-gateway) [![clean-architecture](https://img.shields.io/badge/clean--architecture-10B981?style=flat-square)](skills/architecture/clean-architecture) [![cqrs](https://img.shields.io/badge/cqrs-10B981?style=flat-square)](skills/architecture/cqrs) [![domain-driven-design](https://img.shields.io/badge/domain--driven--design-10B981?style=flat-square)](skills/architecture/domain-driven-design) [![event-driven](https://img.shields.io/badge/event--driven-10B981?style=flat-square)](skills/architecture/event-driven) [![event-sourcing](https://img.shields.io/badge/event--sourcing-10B981?style=flat-square)](skills/architecture/event-sourcing) [![graphql](https://img.shields.io/badge/graphql-10B981?style=flat-square)](skills/architecture/graphql) [![grpc](https://img.shields.io/badge/grpc-10B981?style=flat-square)](skills/architecture/grpc) [![hexagonal](https://img.shields.io/badge/hexagonal-10B981?style=flat-square)](skills/architecture/hexagonal) [![microservices](https://img.shields.io/badge/microservices-10B981?style=flat-square)](skills/architecture/microservices) [![modular-monolith](https://img.shields.io/badge/modular--monolith-10B981?style=flat-square)](skills/architecture/modular-monolith) [![monolith](https://img.shields.io/badge/monolith-10B981?style=flat-square)](skills/architecture/monolith) [![rest-api](https://img.shields.io/badge/rest--api-10B981?style=flat-square)](skills/architecture/rest-api) [![saga](https://img.shields.io/badge/saga-10B981?style=flat-square)](skills/architecture/saga) [![serverless](https://img.shields.io/badge/serverless-10B981?style=flat-square)](skills/architecture/serverless) [![service-mesh](https://img.shields.io/badge/service--mesh-10B981?style=flat-square)](skills/architecture/service-mesh) [![sse](https://img.shields.io/badge/sse-10B981?style=flat-square)](skills/architecture/sse) [![twelve-factor](https://img.shields.io/badge/twelve--factor-10B981?style=flat-square)](skills/architecture/twelve-factor) [![webhooks](https://img.shields.io/badge/webhooks-10B981?style=flat-square)](skills/architecture/webhooks) [![websockets](https://img.shields.io/badge/websockets-10B981?style=flat-square)](skills/architecture/websockets)

### Databases & Storage (`skills/databases`) — 30 Skills

[![arangodb](https://img.shields.io/badge/arangodb-3B82F6?style=flat-square)](skills/databases/arangodb) [![bigquery](https://img.shields.io/badge/bigquery-3B82F6?style=flat-square)](skills/databases/bigquery) [![cassandra](https://img.shields.io/badge/cassandra-3B82F6?style=flat-square)](skills/databases/cassandra) [![clickhouse](https://img.shields.io/badge/clickhouse-3B82F6?style=flat-square)](skills/databases/clickhouse) [![cockroachdb](https://img.shields.io/badge/cockroachdb-3B82F6?style=flat-square)](skills/databases/cockroachdb) [![cosmosdb](https://img.shields.io/badge/cosmosdb-3B82F6?style=flat-square)](skills/databases/cosmosdb) [![couchbase](https://img.shields.io/badge/couchbase-3B82F6?style=flat-square)](skills/databases/couchbase) [![couchdb](https://img.shields.io/badge/couchdb-3B82F6?style=flat-square)](skills/databases/couchdb) [![db2](https://img.shields.io/badge/db2-3B82F6?style=flat-square)](skills/databases/db2) [![duckdb](https://img.shields.io/badge/duckdb-3B82F6?style=flat-square)](skills/databases/duckdb) [![dynamodb](https://img.shields.io/badge/dynamodb-3B82F6?style=flat-square)](skills/databases/dynamodb) [![elasticsearch](https://img.shields.io/badge/elasticsearch-3B82F6?style=flat-square)](skills/databases/elasticsearch) [![firebase](https://img.shields.io/badge/firebase-3B82F6?style=flat-square)](skills/databases/firebase) [![hbase](https://img.shields.io/badge/hbase-3B82F6?style=flat-square)](skills/databases/hbase) [![influxdb](https://img.shields.io/badge/influxdb-3B82F6?style=flat-square)](skills/databases/influxdb) [![mariadb](https://img.shields.io/badge/mariadb-3B82F6?style=flat-square)](skills/databases/mariadb) [![memcached](https://img.shields.io/badge/memcached-3B82F6?style=flat-square)](skills/databases/memcached) [![mongodb](https://img.shields.io/badge/mongodb-3B82F6?style=flat-square)](skills/databases/mongodb) [![mysql](https://img.shields.io/badge/mysql-3B82F6?style=flat-square)](skills/databases/mysql) [![neo4j](https://img.shields.io/badge/neo4j-3B82F6?style=flat-square)](skills/databases/neo4j) [![neon](https://img.shields.io/badge/neon-3B82F6?style=flat-square)](skills/databases/neon) [![oracle](https://img.shields.io/badge/oracle-3B82F6?style=flat-square)](skills/databases/oracle) [![planetscale](https://img.shields.io/badge/planetscale-3B82F6?style=flat-square)](skills/databases/planetscale) [![postgresql](https://img.shields.io/badge/postgresql-3B82F6?style=flat-square)](skills/databases/postgresql) [![redis](https://img.shields.io/badge/redis-3B82F6?style=flat-square)](skills/databases/redis) [![snowflake](https://img.shields.io/badge/snowflake-3B82F6?style=flat-square)](skills/databases/snowflake) [![sqlite](https://img.shields.io/badge/sqlite-3B82F6?style=flat-square)](skills/databases/sqlite) [![sqlserver](https://img.shields.io/badge/sqlserver-3B82F6?style=flat-square)](skills/databases/sqlserver) [![supabase](https://img.shields.io/badge/supabase-3B82F6?style=flat-square)](skills/databases/supabase) [![timescaledb](https://img.shields.io/badge/timescaledb-3B82F6?style=flat-square)](skills/databases/timescaledb)

### DevOps & Cloud Native (`skills/devops`) — 50 Skills

[![ansible](https://img.shields.io/badge/ansible-F97316?style=flat-square)](skills/devops/ansible) [![apache](https://img.shields.io/badge/apache-F97316?style=flat-square)](skills/devops/apache) [![argocd](https://img.shields.io/badge/argocd-F97316?style=flat-square)](skills/devops/argocd) [![aws](https://img.shields.io/badge/aws-F97316?style=flat-square)](skills/devops/aws) [![awscli](https://img.shields.io/badge/awscli-F97316?style=flat-square)](skills/devops/awscli) [![azure](https://img.shields.io/badge/azure-F97316?style=flat-square)](skills/devops/azure) [![azurecli](https://img.shields.io/badge/azurecli-F97316?style=flat-square)](skills/devops/azurecli) [![caddy](https://img.shields.io/badge/caddy-F97316?style=flat-square)](skills/devops/caddy) [![cargo](https://img.shields.io/badge/cargo-F97316?style=flat-square)](skills/devops/cargo) [![circleci](https://img.shields.io/badge/circleci-F97316?style=flat-square)](skills/devops/circleci) [![cloudflare](https://img.shields.io/badge/cloudflare-F97316?style=flat-square)](skills/devops/cloudflare) [![consul](https://img.shields.io/badge/consul-F97316?style=flat-square)](skills/devops/consul) [![datadog](https://img.shields.io/badge/datadog-F97316?style=flat-square)](skills/devops/datadog) [![digitalocean](https://img.shields.io/badge/digitalocean-F97316?style=flat-square)](skills/devops/digitalocean) [![docker](https://img.shields.io/badge/docker-F97316?style=flat-square)](skills/devops/docker) [![fly-io](https://img.shields.io/badge/fly--io-F97316?style=flat-square)](skills/devops/fly-io) [![gcloud](https://img.shields.io/badge/gcloud-F97316?style=flat-square)](skills/devops/gcloud) [![gcp](https://img.shields.io/badge/gcp-F97316?style=flat-square)](skills/devops/gcp) [![github-actions](https://img.shields.io/badge/github--actions-F97316?style=flat-square)](skills/devops/github-actions) [![gitlab-ci](https://img.shields.io/badge/gitlab--ci-F97316?style=flat-square)](skills/devops/gitlab-ci) [![grafana](https://img.shields.io/badge/grafana-F97316?style=flat-square)](skills/devops/grafana) [![haproxy](https://img.shields.io/badge/haproxy-F97316?style=flat-square)](skills/devops/haproxy) [![helm](https://img.shields.io/badge/helm-F97316?style=flat-square)](skills/devops/helm) [![heroku](https://img.shields.io/badge/heroku-F97316?style=flat-square)](skills/devops/heroku) [![homebrew](https://img.shields.io/badge/homebrew-F97316?style=flat-square)](skills/devops/homebrew) [![istio](https://img.shields.io/badge/istio-F97316?style=flat-square)](skills/devops/istio) [![jenkins](https://img.shields.io/badge/jenkins-F97316?style=flat-square)](skills/devops/jenkins) [![kubernetes](https://img.shields.io/badge/kubernetes-F97316?style=flat-square)](skills/devops/kubernetes) [![linkerd](https://img.shields.io/badge/linkerd-F97316?style=flat-square)](skills/devops/linkerd) [![linode](https://img.shields.io/badge/linode-F97316?style=flat-square)](skills/devops/linode) [![netlify](https://img.shields.io/badge/netlify-F97316?style=flat-square)](skills/devops/netlify) [![nginx](https://img.shields.io/badge/nginx-F97316?style=flat-square)](skills/devops/nginx) [![nomad](https://img.shields.io/badge/nomad-F97316?style=flat-square)](skills/devops/nomad) [![npm](https://img.shields.io/badge/npm-F97316?style=flat-square)](skills/devops/npm) [![openshift](https://img.shields.io/badge/openshift-F97316?style=flat-square)](skills/devops/openshift) [![packer](https://img.shields.io/badge/packer-F97316?style=flat-square)](skills/devops/packer) [![pip](https://img.shields.io/badge/pip-F97316?style=flat-square)](skills/devops/pip) [![pnpm](https://img.shields.io/badge/pnpm-F97316?style=flat-square)](skills/devops/pnpm) [![podman](https://img.shields.io/badge/podman-F97316?style=flat-square)](skills/devops/podman) [![prometheus](https://img.shields.io/badge/prometheus-F97316?style=flat-square)](skills/devops/prometheus) [![pulumi](https://img.shields.io/badge/pulumi-F97316?style=flat-square)](skills/devops/pulumi) [![railway](https://img.shields.io/badge/railway-F97316?style=flat-square)](skills/devops/railway) [![rancher](https://img.shields.io/badge/rancher-F97316?style=flat-square)](skills/devops/rancher) [![render](https://img.shields.io/badge/render-F97316?style=flat-square)](skills/devops/render) [![sentry](https://img.shields.io/badge/sentry-F97316?style=flat-square)](skills/devops/sentry) [![terraform](https://img.shields.io/badge/terraform-F97316?style=flat-square)](skills/devops/terraform) [![traefik](https://img.shields.io/badge/traefik-F97316?style=flat-square)](skills/devops/traefik) [![vagrant](https://img.shields.io/badge/vagrant-F97316?style=flat-square)](skills/devops/vagrant) [![vercel](https://img.shields.io/badge/vercel-F97316?style=flat-square)](skills/devops/vercel) [![yarn](https://img.shields.io/badge/yarn-F97316?style=flat-square)](skills/devops/yarn)

### Web & App Frameworks (`skills/frameworks`) — 47 Skills

[![actix](https://img.shields.io/badge/actix-EC4899?style=flat-square)](skills/frameworks/actix) [![angular](https://img.shields.io/badge/angular-EC4899?style=flat-square)](skills/frameworks/angular) [![aspnet-core](https://img.shields.io/badge/aspnet--core-EC4899?style=flat-square)](skills/frameworks/aspnet-core) [![astro](https://img.shields.io/badge/astro-EC4899?style=flat-square)](skills/frameworks/astro) [![axum](https://img.shields.io/badge/axum-EC4899?style=flat-square)](skills/frameworks/axum) [![blazor](https://img.shields.io/badge/blazor-EC4899?style=flat-square)](skills/frameworks/blazor) [![bootstrap](https://img.shields.io/badge/bootstrap-EC4899?style=flat-square)](skills/frameworks/bootstrap) [![bun](https://img.shields.io/badge/bun-EC4899?style=flat-square)](skills/frameworks/bun) [![chakraui](https://img.shields.io/badge/chakraui-EC4899?style=flat-square)](skills/frameworks/chakraui) [![deno](https://img.shields.io/badge/deno-EC4899?style=flat-square)](skills/frameworks/deno) [![django](https://img.shields.io/badge/django-EC4899?style=flat-square)](skills/frameworks/django) [![drizzle](https://img.shields.io/badge/drizzle-EC4899?style=flat-square)](skills/frameworks/drizzle) [![echo](https://img.shields.io/badge/echo-EC4899?style=flat-square)](skills/frameworks/echo) [![electron](https://img.shields.io/badge/electron-EC4899?style=flat-square)](skills/frameworks/electron) [![express](https://img.shields.io/badge/express-EC4899?style=flat-square)](skills/frameworks/express) [![fastapi](https://img.shields.io/badge/fastapi-EC4899?style=flat-square)](skills/frameworks/fastapi) [![fiber](https://img.shields.io/badge/fiber-EC4899?style=flat-square)](skills/frameworks/fiber) [![flask](https://img.shields.io/badge/flask-EC4899?style=flat-square)](skills/frameworks/flask) [![gatsby](https://img.shields.io/badge/gatsby-EC4899?style=flat-square)](skills/frameworks/gatsby) [![gin](https://img.shields.io/badge/gin-EC4899?style=flat-square)](skills/frameworks/gin) [![hono](https://img.shields.io/badge/hono-EC4899?style=flat-square)](skills/frameworks/hono) [![htmx](https://img.shields.io/badge/htmx-EC4899?style=flat-square)](skills/frameworks/htmx) [![jquery](https://img.shields.io/badge/jquery-EC4899?style=flat-square)](skills/frameworks/jquery) [![laravel](https://img.shields.io/badge/laravel-EC4899?style=flat-square)](skills/frameworks/laravel) [![materialui](https://img.shields.io/badge/materialui-EC4899?style=flat-square)](skills/frameworks/materialui) [![nestjs](https://img.shields.io/badge/nestjs-EC4899?style=flat-square)](skills/frameworks/nestjs) [![nextjs](https://img.shields.io/badge/nextjs-EC4899?style=flat-square)](skills/frameworks/nextjs) [![nodejs](https://img.shields.io/badge/nodejs-EC4899?style=flat-square)](skills/frameworks/nodejs) [![nuxt](https://img.shields.io/badge/nuxt-EC4899?style=flat-square)](skills/frameworks/nuxt) [![phoenix](https://img.shields.io/badge/phoenix-EC4899?style=flat-square)](skills/frameworks/phoenix) [![prisma](https://img.shields.io/badge/prisma-EC4899?style=flat-square)](skills/frameworks/prisma) [![rails](https://img.shields.io/badge/rails-EC4899?style=flat-square)](skills/frameworks/rails) [![react](https://img.shields.io/badge/react-EC4899?style=flat-square)](skills/frameworks/react) [![remix](https://img.shields.io/badge/remix-EC4899?style=flat-square)](skills/frameworks/remix) [![sanity](https://img.shields.io/badge/sanity-EC4899?style=flat-square)](skills/frameworks/sanity) [![shadcnui](https://img.shields.io/badge/shadcnui-EC4899?style=flat-square)](skills/frameworks/shadcnui) [![solidjs](https://img.shields.io/badge/solidjs-EC4899?style=flat-square)](skills/frameworks/solidjs) [![spring-boot](https://img.shields.io/badge/spring--boot-EC4899?style=flat-square)](skills/frameworks/spring-boot) [![strapi](https://img.shields.io/badge/strapi-EC4899?style=flat-square)](skills/frameworks/strapi) [![svelte](https://img.shields.io/badge/svelte-EC4899?style=flat-square)](skills/frameworks/svelte) [![sveltekit](https://img.shields.io/badge/sveltekit-EC4899?style=flat-square)](skills/frameworks/sveltekit) [![symfony](https://img.shields.io/badge/symfony-EC4899?style=flat-square)](skills/frameworks/symfony) [![tailwindcss](https://img.shields.io/badge/tailwindcss-EC4899?style=flat-square)](skills/frameworks/tailwindcss) [![tauri](https://img.shields.io/badge/tauri-EC4899?style=flat-square)](skills/frameworks/tauri) [![vue](https://img.shields.io/badge/vue-EC4899?style=flat-square)](skills/frameworks/vue) [![vuetify](https://img.shields.io/badge/vuetify-EC4899?style=flat-square)](skills/frameworks/vuetify) [![wordpress](https://img.shields.io/badge/wordpress-EC4899?style=flat-square)](skills/frameworks/wordpress)

### Programming Languages (`skills/languages`) — 41 Skills

[![assembly](https://img.shields.io/badge/assembly-F59E0B?style=flat-square)](skills/languages/assembly) [![bash](https://img.shields.io/badge/bash-F59E0B?style=flat-square)](skills/languages/bash) [![c](https://img.shields.io/badge/c-F59E0B?style=flat-square)](skills/languages/c) [![clojure](https://img.shields.io/badge/clojure-F59E0B?style=flat-square)](skills/languages/clojure) [![cobol](https://img.shields.io/badge/cobol-F59E0B?style=flat-square)](skills/languages/cobol) [![cpp](https://img.shields.io/badge/cpp-F59E0B?style=flat-square)](skills/languages/cpp) [![crystal](https://img.shields.io/badge/crystal-F59E0B?style=flat-square)](skills/languages/crystal) [![csharp](https://img.shields.io/badge/csharp-F59E0B?style=flat-square)](skills/languages/csharp) [![dart](https://img.shields.io/badge/dart-F59E0B?style=flat-square)](skills/languages/dart) [![delphi](https://img.shields.io/badge/delphi-F59E0B?style=flat-square)](skills/languages/delphi) [![elixir](https://img.shields.io/badge/elixir-F59E0B?style=flat-square)](skills/languages/elixir) [![erlang](https://img.shields.io/badge/erlang-F59E0B?style=flat-square)](skills/languages/erlang) [![fortran](https://img.shields.io/badge/fortran-F59E0B?style=flat-square)](skills/languages/fortran) [![fsharp](https://img.shields.io/badge/fsharp-F59E0B?style=flat-square)](skills/languages/fsharp) [![go](https://img.shields.io/badge/go-F59E0B?style=flat-square)](skills/languages/go) [![groovy](https://img.shields.io/badge/groovy-F59E0B?style=flat-square)](skills/languages/groovy) [![haskell](https://img.shields.io/badge/haskell-F59E0B?style=flat-square)](skills/languages/haskell) [![html-css](https://img.shields.io/badge/html--css-F59E0B?style=flat-square)](skills/languages/html-css) [![java](https://img.shields.io/badge/java-F59E0B?style=flat-square)](skills/languages/java) [![javascript](https://img.shields.io/badge/javascript-F59E0B?style=flat-square)](skills/languages/javascript) [![julia](https://img.shields.io/badge/julia-F59E0B?style=flat-square)](skills/languages/julia) [![kotlin](https://img.shields.io/badge/kotlin-F59E0B?style=flat-square)](skills/languages/kotlin) [![lua](https://img.shields.io/badge/lua-F59E0B?style=flat-square)](skills/languages/lua) [![nim](https://img.shields.io/badge/nim-F59E0B?style=flat-square)](skills/languages/nim) [![objective-c](https://img.shields.io/badge/objective--c-F59E0B?style=flat-square)](skills/languages/objective-c) [![ocaml](https://img.shields.io/badge/ocaml-F59E0B?style=flat-square)](skills/languages/ocaml) [![perl](https://img.shields.io/badge/perl-F59E0B?style=flat-square)](skills/languages/perl) [![php](https://img.shields.io/badge/php-F59E0B?style=flat-square)](skills/languages/php) [![powershell](https://img.shields.io/badge/powershell-F59E0B?style=flat-square)](skills/languages/powershell) [![python](https://img.shields.io/badge/python-F59E0B?style=flat-square)](skills/languages/python) [![r](https://img.shields.io/badge/r-F59E0B?style=flat-square)](skills/languages/r) [![ruby](https://img.shields.io/badge/ruby-F59E0B?style=flat-square)](skills/languages/ruby) [![rust](https://img.shields.io/badge/rust-F59E0B?style=flat-square)](skills/languages/rust) [![scala](https://img.shields.io/badge/scala-F59E0B?style=flat-square)](skills/languages/scala) [![solidity](https://img.shields.io/badge/solidity-F59E0B?style=flat-square)](skills/languages/solidity) [![sql](https://img.shields.io/badge/sql-F59E0B?style=flat-square)](skills/languages/sql) [![swift](https://img.shields.io/badge/swift-F59E0B?style=flat-square)](skills/languages/swift) [![typescript](https://img.shields.io/badge/typescript-F59E0B?style=flat-square)](skills/languages/typescript) [![v](https://img.shields.io/badge/v-F59E0B?style=flat-square)](skills/languages/v) [![vbnet](https://img.shields.io/badge/vbnet-F59E0B?style=flat-square)](skills/languages/vbnet) [![zig](https://img.shields.io/badge/zig-F59E0B?style=flat-square)](skills/languages/zig)

### Mobile Development (`skills/mobile`) — 13 Skills

[![android-sdk](https://img.shields.io/badge/android--sdk-06B6D4?style=flat-square)](skills/mobile/android-sdk) [![capacitor](https://img.shields.io/badge/capacitor-06B6D4?style=flat-square)](skills/mobile/capacitor) [![cordova](https://img.shields.io/badge/cordova-06B6D4?style=flat-square)](skills/mobile/cordova) [![expo](https://img.shields.io/badge/expo-06B6D4?style=flat-square)](skills/mobile/expo) [![flutter](https://img.shields.io/badge/flutter-06B6D4?style=flat-square)](skills/mobile/flutter) [![ionic](https://img.shields.io/badge/ionic-06B6D4?style=flat-square)](skills/mobile/ionic) [![jetpack-compose](https://img.shields.io/badge/jetpack--compose-06B6D4?style=flat-square)](skills/mobile/jetpack-compose) [![kotlin-multiplatform](https://img.shields.io/badge/kotlin--multiplatform-06B6D4?style=flat-square)](skills/mobile/kotlin-multiplatform) [![nativescript](https://img.shields.io/badge/nativescript-06B6D4?style=flat-square)](skills/mobile/nativescript) [![react-native](https://img.shields.io/badge/react--native-06B6D4?style=flat-square)](skills/mobile/react-native) [![swiftui](https://img.shields.io/badge/swiftui-06B6D4?style=flat-square)](skills/mobile/swiftui) [![uikit](https://img.shields.io/badge/uikit-06B6D4?style=flat-square)](skills/mobile/uikit) [![xamarin](https://img.shields.io/badge/xamarin-06B6D4?style=flat-square)](skills/mobile/xamarin)

### Security & Compliance (`skills/security`) — 19 Skills

[![auth0](https://img.shields.io/badge/auth0-EF4444?style=flat-square)](skills/security/auth0) [![bcrypt](https://img.shields.io/badge/bcrypt-EF4444?style=flat-square)](skills/security/bcrypt) [![burpsuite](https://img.shields.io/badge/burpsuite-EF4444?style=flat-square)](skills/security/burpsuite) [![certbot](https://img.shields.io/badge/certbot-EF4444?style=flat-square)](skills/security/certbot) [![clerk](https://img.shields.io/badge/clerk-EF4444?style=flat-square)](skills/security/clerk) [![dependabot](https://img.shields.io/badge/dependabot-EF4444?style=flat-square)](skills/security/dependabot) [![jwt](https://img.shields.io/badge/jwt-EF4444?style=flat-square)](skills/security/jwt) [![keycloak](https://img.shields.io/badge/keycloak-EF4444?style=flat-square)](skills/security/keycloak) [![nextauth](https://img.shields.io/badge/nextauth-EF4444?style=flat-square)](skills/security/nextauth) [![oauth](https://img.shields.io/badge/oauth-EF4444?style=flat-square)](skills/security/oauth) [![okta](https://img.shields.io/badge/okta-EF4444?style=flat-square)](skills/security/okta) [![openid-connect](https://img.shields.io/badge/openid--connect-EF4444?style=flat-square)](skills/security/openid-connect) [![owasp-zap](https://img.shields.io/badge/owasp--zap-EF4444?style=flat-square)](skills/security/owasp-zap) [![passport](https://img.shields.io/badge/passport-EF4444?style=flat-square)](skills/security/passport) [![renovate](https://img.shields.io/badge/renovate-EF4444?style=flat-square)](skills/security/renovate) [![snyk](https://img.shields.io/badge/snyk-EF4444?style=flat-square)](skills/security/snyk) [![sonarqube](https://img.shields.io/badge/sonarqube-EF4444?style=flat-square)](skills/security/sonarqube) [![trivy](https://img.shields.io/badge/trivy-EF4444?style=flat-square)](skills/security/trivy) [![vault](https://img.shields.io/badge/vault-EF4444?style=flat-square)](skills/security/vault)

### Testing & Quality Assurance (`skills/testing`) — 25 Skills

[![appium](https://img.shields.io/badge/appium-84CC16?style=flat-square)](skills/testing/appium) [![cargo-test](https://img.shields.io/badge/cargo--test-84CC16?style=flat-square)](skills/testing/cargo-test) [![chai](https://img.shields.io/badge/chai-84CC16?style=flat-square)](skills/testing/chai) [![cypress](https://img.shields.io/badge/cypress-84CC16?style=flat-square)](skills/testing/cypress) [![detox](https://img.shields.io/badge/detox-84CC16?style=flat-square)](skills/testing/detox) [![gatling](https://img.shields.io/badge/gatling-84CC16?style=flat-square)](skills/testing/gatling) [![go-test](https://img.shields.io/badge/go--test-84CC16?style=flat-square)](skills/testing/go-test) [![jest](https://img.shields.io/badge/jest-84CC16?style=flat-square)](skills/testing/jest) [![junit](https://img.shields.io/badge/junit-84CC16?style=flat-square)](skills/testing/junit) [![k6](https://img.shields.io/badge/k6-84CC16?style=flat-square)](skills/testing/k6) [![locust](https://img.shields.io/badge/locust-84CC16?style=flat-square)](skills/testing/locust) [![mocha](https://img.shields.io/badge/mocha-84CC16?style=flat-square)](skills/testing/mocha) [![nunit](https://img.shields.io/badge/nunit-84CC16?style=flat-square)](skills/testing/nunit) [![phpunit](https://img.shields.io/badge/phpunit-84CC16?style=flat-square)](skills/testing/phpunit) [![playwright](https://img.shields.io/badge/playwright-84CC16?style=flat-square)](skills/testing/playwright) [![puppeteer](https://img.shields.io/badge/puppeteer-84CC16?style=flat-square)](skills/testing/puppeteer) [![pytest](https://img.shields.io/badge/pytest-84CC16?style=flat-square)](skills/testing/pytest) [![rspec](https://img.shields.io/badge/rspec-84CC16?style=flat-square)](skills/testing/rspec) [![selenium](https://img.shields.io/badge/selenium-84CC16?style=flat-square)](skills/testing/selenium) [![storybook](https://img.shields.io/badge/storybook-84CC16?style=flat-square)](skills/testing/storybook) [![testing-library](https://img.shields.io/badge/testing--library-84CC16?style=flat-square)](skills/testing/testing-library) [![testng](https://img.shields.io/badge/testng-84CC16?style=flat-square)](skills/testing/testng) [![vitest](https://img.shields.io/badge/vitest-84CC16?style=flat-square)](skills/testing/vitest) [![webdriver](https://img.shields.io/badge/webdriver-84CC16?style=flat-square)](skills/testing/webdriver) [![xunit](https://img.shields.io/badge/xunit-84CC16?style=flat-square)](skills/testing/xunit)

### Developer Tools & Workflows (`skills/tools`) — 60 Skills

[![android-studio](https://img.shields.io/badge/android--studio-6366F1?style=flat-square)](skills/tools/android-studio) [![atom](https://img.shields.io/badge/atom-6366F1?style=flat-square)](skills/tools/atom) [![babel](https://img.shields.io/badge/babel-6366F1?style=flat-square)](skills/tools/babel) [![biome](https://img.shields.io/badge/biome-6366F1?style=flat-square)](skills/tools/biome) [![bitbucket](https://img.shields.io/badge/bitbucket-6366F1?style=flat-square)](skills/tools/bitbucket) [![confluence](https://img.shields.io/badge/confluence-6366F1?style=flat-square)](skills/tools/confluence) [![cursor](https://img.shields.io/badge/cursor-6366F1?style=flat-square)](skills/tools/cursor) [![datagrip](https://img.shields.io/badge/datagrip-6366F1?style=flat-square)](skills/tools/datagrip) [![dbeaver](https://img.shields.io/badge/dbeaver-6366F1?style=flat-square)](skills/tools/dbeaver) [![discord](https://img.shields.io/badge/discord-6366F1?style=flat-square)](skills/tools/discord) [![docker-desktop](https://img.shields.io/badge/docker--desktop-6366F1?style=flat-square)](skills/tools/docker-desktop) [![eclipse](https://img.shields.io/badge/eclipse-6366F1?style=flat-square)](skills/tools/eclipse) [![emacs](https://img.shields.io/badge/emacs-6366F1?style=flat-square)](skills/tools/emacs) [![esbuild](https://img.shields.io/badge/esbuild-6366F1?style=flat-square)](skills/tools/esbuild) [![eslint](https://img.shields.io/badge/eslint-6366F1?style=flat-square)](skills/tools/eslint) [![figma](https://img.shields.io/badge/figma-6366F1?style=flat-square)](skills/tools/figma) [![fish](https://img.shields.io/badge/fish-6366F1?style=flat-square)](skills/tools/fish) [![git](https://img.shields.io/badge/git-6366F1?style=flat-square)](skills/tools/git) [![github](https://img.shields.io/badge/github-6366F1?style=flat-square)](skills/tools/github) [![gitlab](https://img.shields.io/badge/gitlab-6366F1?style=flat-square)](skills/tools/gitlab) [![goland](https://img.shields.io/badge/goland-6366F1?style=flat-square)](skills/tools/goland) [![httpie](https://img.shields.io/badge/httpie-6366F1?style=flat-square)](skills/tools/httpie) [![insomnia](https://img.shields.io/badge/insomnia-6366F1?style=flat-square)](skills/tools/insomnia) [![intellij](https://img.shields.io/badge/intellij-6366F1?style=flat-square)](skills/tools/intellij) [![iterm2](https://img.shields.io/badge/iterm2-6366F1?style=flat-square)](skills/tools/iterm2) [![jira](https://img.shields.io/badge/jira-6366F1?style=flat-square)](skills/tools/jira) [![k9s](https://img.shields.io/badge/k9s-6366F1?style=flat-square)](skills/tools/k9s) [![lazygit](https://img.shields.io/badge/lazygit-6366F1?style=flat-square)](skills/tools/lazygit) [![lens](https://img.shields.io/badge/lens-6366F1?style=flat-square)](skills/tools/lens) [![linear](https://img.shields.io/badge/linear-6366F1?style=flat-square)](skills/tools/linear) [![neovim](https://img.shields.io/badge/neovim-6366F1?style=flat-square)](skills/tools/neovim) [![notepad-plus-plus](https://img.shields.io/badge/notepad--plus--plus-6366F1?style=flat-square)](skills/tools/notepad-plus-plus) [![notion](https://img.shields.io/badge/notion-6366F1?style=flat-square)](skills/tools/notion) [![obsidian](https://img.shields.io/badge/obsidian-6366F1?style=flat-square)](skills/tools/obsidian) [![parcel](https://img.shields.io/badge/parcel-6366F1?style=flat-square)](skills/tools/parcel) [![phpstorm](https://img.shields.io/badge/phpstorm-6366F1?style=flat-square)](skills/tools/phpstorm) [![postman](https://img.shields.io/badge/postman-6366F1?style=flat-square)](skills/tools/postman) [![prettier](https://img.shields.io/badge/prettier-6366F1?style=flat-square)](skills/tools/prettier) [![pycharm](https://img.shields.io/badge/pycharm-6366F1?style=flat-square)](skills/tools/pycharm) [![rider](https://img.shields.io/badge/rider-6366F1?style=flat-square)](skills/tools/rider) [![rollup](https://img.shields.io/badge/rollup-6366F1?style=flat-square)](skills/tools/rollup) [![rubymine](https://img.shields.io/badge/rubymine-6366F1?style=flat-square)](skills/tools/rubymine) [![sketch](https://img.shields.io/badge/sketch-6366F1?style=flat-square)](skills/tools/sketch) [![slack](https://img.shields.io/badge/slack-6366F1?style=flat-square)](skills/tools/slack) [![sublime-text](https://img.shields.io/badge/sublime--text-6366F1?style=flat-square)](skills/tools/sublime-text) [![swc](https://img.shields.io/badge/swc-6366F1?style=flat-square)](skills/tools/swc) [![tableplus](https://img.shields.io/badge/tableplus-6366F1?style=flat-square)](skills/tools/tableplus) [![tig](https://img.shields.io/badge/tig-6366F1?style=flat-square)](skills/tools/tig) [![tmux](https://img.shields.io/badge/tmux-6366F1?style=flat-square)](skills/tools/tmux) [![turbopack](https://img.shields.io/badge/turbopack-6366F1?style=flat-square)](skills/tools/turbopack) [![vim](https://img.shields.io/badge/vim-6366F1?style=flat-square)](skills/tools/vim) [![visual-studio](https://img.shields.io/badge/visual--studio-6366F1?style=flat-square)](skills/tools/visual-studio) [![vite](https://img.shields.io/badge/vite-6366F1?style=flat-square)](skills/tools/vite) [![vscode](https://img.shields.io/badge/vscode-6366F1?style=flat-square)](skills/tools/vscode) [![warp](https://img.shields.io/badge/warp-6366F1?style=flat-square)](skills/tools/warp) [![webpack](https://img.shields.io/badge/webpack-6366F1?style=flat-square)](skills/tools/webpack) [![webstorm](https://img.shields.io/badge/webstorm-6366F1?style=flat-square)](skills/tools/webstorm) [![xcode](https://img.shields.io/badge/xcode-6366F1?style=flat-square)](skills/tools/xcode) [![zed](https://img.shields.io/badge/zed-6366F1?style=flat-square)](skills/tools/zed) [![zsh](https://img.shields.io/badge/zsh-6366F1?style=flat-square)](skills/tools/zsh)

---

## Skill Anatomy

Each skill is a self-contained directory containing a `SKILL.md` file following [template/SKILL.md](template/SKILL.md):

```text
skill-name/
└── SKILL.md          # Instructions, metadata, patterns & diagnostic matrix
```

### SKILL.md Structure

````markdown
---
name: template
description: Expert [skill-name] assistance covering [feature 1], [feature 2], and [feature 3]. Use when [working with X], [debugging Y], or [implementing Z].
---

# Skill Name

Brief overview of what this skill does and the key capabilities it provides.

## When to Use

- Trigger phrase or scenario 1
- Trigger phrase or scenario 2
- Trigger phrase or scenario 3

## Quick Start

```language
// Minimal working example - copy-paste ready
// Include essential imports and setup
```

## Core Concepts

### Concept 1

Explanation of fundamental concept with practical context.

```language
// Code example demonstrating the concept
```

### Concept 2

Another essential concept with clear explanation.

```language
// Practical code example
```

## Common Patterns

### Pattern Name

**Problem**: What challenge does this solve?

**Solution**:

```language
// Recommended approach with comments
```

## Best Practices

**Do**:

- Practice 1 with rationale
- Practice 2 with explanation

**Don't**:

- Anti-pattern 1 and why
- Anti-pattern 2 and the alternative

## Troubleshooting

| Error         | Cause          | Solution   |
| ------------- | -------------- | ---------- |
| Error message | Why it happens | How to fix |

## References

- [Documentation](https://example.com)
````

---

## Directory Structure

```text
agent-skills/
├── skills/                    # All skill definitions
│   ├── ai-ml/                 # ML frameworks, LLMs, data science
│   ├── architecture/          # System design, API patterns, distributed architecture
│   ├── databases/             # SQL, NoSQL, Vector DBs, ORMs
│   ├── devops/                # Containers, CI/CD, IaC, Cloud
│   ├── frameworks/            # Frontend, backend, fullstack frameworks
│   ├── languages/             # Programming languages & runtimes
│   ├── mobile/                # iOS, Android, cross-platform
│   ├── security/              # Auth, encryption, secure coding
│   ├── testing/               # Unit, E2E, performance testing
│   └── tools/                 # Developer tools, IDEs, bundlers, CLIs
├── template/                  # Standardized skill template
│   └── SKILL.md
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # Catalog documentation
```

---

## Learn More

- [agentskills.io](https://agentskills.io/) - Official Agent Skills Specification
- [skills.sh](https://skills.sh/) - Interactive Skills Directory

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

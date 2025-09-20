# Plan de création de l'API (FastAPI) — ふうりん

Ce fichier suit l'avancement de l'API consommée par le front Svelte. L'objectif initial est le tracking d'activité et des statistiques (pas de leçons).

Principes
- Python 3.12 + FastAPI + Uvicorn.
- DB: PostgreSQL (schéma basé sur model.md, sans "lessons").
- Auth simple (JWT) ultérieurement — pour l’instant endpoints publics/maquettés.
- Versionnement d’API: /api/v1.
- Architecture & conventions: voir `api/ARCHITECTURE.md` (organisation des dossiers, versionnement, bonnes pratiques FastAPI).

Découpage par phases

Phase 0 — Bootstrap (cette PR)
- [x] Squelette FastAPI (health, version).
- [x] Dockerfile API.
- [x] Docker Compose racine avec Postgres + API + Front.
- [x] Variables d’environnement de connexion DB (sans code de connexion encore).
- [x] Document de suivi (ce fichier).

Phase 1 — Connexion DB & migrations
- [x] Ajouter SQLAlchemy + Alembic.
- [x] Configurer la connexion PostgreSQL via env (DATABASE_URL).
- [x] Créer migrations initiales minimales: users, works, study_sessions, activity_events, achievements, goals, goal_progress, notifications, leaderboards.
- [x] Script de seed basique (1 user de test, 2 works, quelques sessions et events).

Phase 2 — Endpoints lecture (read-only) pour dashboard/feed
- [x] GET /api/v1/health (déjà /health à la racine)
- [x] GET /api/v1/works — liste d’œuvres (type, titre)
- [x] GET /api/v1/reading-speeds?work_id= — séries pour le graphe
- [x] GET /api/v1/users — liste d’utilisateurs (dev)
- [x] GET /api/v1/users/{user_id} — détail utilisateur (dev)
- [x] GET /api/v1/users/{user_id}/summary — métriques cartes (words_learned, time_studied, streak)
- [x] GET /api/v1/activity-events?user_id=&limit= — feed d’activité récent
- [x] GET /api/v1/study-sessions?user_id=&work_id=&limit= — sessions
- [x] GET /api/v1/stats/daily?user_id=&start=&end= — minutes/words par jour (pour heatmap)
- [x] GET /api/v1/stats/weekly?user_id=&week=YYYY-Www — minutes par jour de la semaine
- [x] Refactor routeurs v1 en modules par entité; suppression des routes /me/* (dépréciées)

Notes: les anciens endpoints /api/v1/me/* restent présents pour transition mais seront supprimés (deprecated).

Phase 3 — Endpoints écriture (log d’activité)
- [ ] POST /api/v1/study-sessions — créer/terminer une session
- [ ] POST /api/v1/activity-events — enregistrer une entrée libre (summary + metadata)
- [ ] POST /api/v1/goals — créer objectif (daily/weekly/monthly)

Phase 4 — Auth & users
- [ ] POST /api/v1/auth/register — inscription (optionnel tôt)
- [ ] POST /api/v1/auth/login — JWT
- [ ] GET /api/v1/me — profil

Phase 5 — Agrégations & perfs
- [ ] Vues matérialisées (mv_user_daily_activity, mv_weekly_study_time, mv_user_streaks)
- [ ] Jobs de refresh (cron/worker) ou refresh-on-write simple

Schémas de données (minimal pour Phase 1)
- users(id, email, password_hash?, display_name, timezone, created_at)
- works(id, title, type, author?, difficulty_level?, source_url?, metadata, created_at)
- study_sessions(id, user_id, started_at, ended_at, duration_sec, modality, work_id?, work_segment_id?, words_reviewed?, words_learned?, notes?)
- activity_events(id, user_id, occurred_at, type, ref_kind, ref_id?, summary, metadata, visibility)
- reading_speeds(id, user_id, work_id, measured_at, chars_per_min, method)
- achievements_catalog(id, code, name, description, icon, criteria)
- user_achievements(user_id, achievement_id, unlocked_at, is_new)
- goals(id, user_id, period, metric, target, start_date, end_date, created_at)
- goal_progress(goal_id, measured_at, value)
- notifications(id, user_id, type, title, body, created_at, read_at?)
- leaderboards(id, scope, metric, period, created_at)
- leaderboard_entries(leaderboard_id, user_id, score, rank, computed_at)

Contrats API (brouillon)
- Summary
  - total_words_learned: number
  - study_time_minutes_7d: number
  - streak_days: number
- ActivityItem
  - id, occurred_at, type, summary, work? {id,title,type}
- StudySessionCreate
  - modality: enum
  - work_id?: uuid
  - started_at?: iso, ended_at?: iso, notes?: string

Env & lancement (dev rapide)
- docker compose up --build
- API: http://localhost:8000 (docs Swagger /docs)
- Front: http://localhost:3000
- Postgres: localhost:5432 (db: fuurin, user: fuurin, pass: fuurin)

Variables d’environnement (service api)
- DATABASE_URL=postgresql+psycopg://fuurin:fuurin@db:5432/fuurin
- APP_ENV=development|production

Notes
- Pas de champ language sur works (toutes les œuvres sont en japonais).
- Pas de tables de leçons pour l’instant.
- Le tracking d’activité reste la priorité.

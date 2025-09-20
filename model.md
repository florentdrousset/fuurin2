# Modèle de données (Proposition) — ふうりん

Ce document propose un modèle de base de données pour ふうりん, une plateforme d’apprentissage du japonais. Il est basé sur l’analyse du code front (Svelte) présent dans ce dépôt et des fonctionnalités exposées dans l’UI. Aucune API/back‑end n’étant incluse dans ce repo (dossier `api` vide), certaines hypothèses sont formulées. Le schéma proposé vise une base relationnelle (PostgreSQL recommandé) avec quelques suggestions annexes pour l’analytique et la recherche.

Résumé des fonctionnalités identifiées dans l’UI
- Authentification / Profil utilisateur (icône profil, paramètres)
- Streak d’étude (Study Streak)
- Statistiques:
  - Mots appris (Words Learned)
  - Temps d’étude (Time Studied)
- Heatmap d’activité d’apprentissage (activité quotidienne sur l’année)
- Réalisations (Achievements)
- Objectifs (Goals) quotidiens/hebdomadaires/mensuels
- Actions rapides (Practice / Listen / Write / Speak)
- Tableau d’entrées récentes (Recent Entries)
- Graphiques:
  - Répartition de la consommation média (Media Consumption: livres, manga, JV, anime)
  - Temps d’étude hebdomadaire (Weekly Study Time)
  - Vitesse de lecture par oeuvre (Reading Speed by Work)
- Fil d’activité (Activity Feed)
- Rubriques prévues (placeholders) : Leaderboard, Library (Ressources), Stats (Analytics), Subscribe (Premium), Submit (Upload), Profile (Settings)

Principes de conception
- Normalisation modérée (3NF) pour cohérence, avec tables de faits pour l’activité et l’étude, et tables de dimensions pour utilisateurs, œuvres, items linguistiques.
- Clés primaires sur identifiants UUID (v4) pour simplicité côté front; clés naturelles possibles selon choix.
- Horodatage systématique (created_at, updated_at), soft delete via deleted_at si utile.
- Contrainte d’intégrité référentielle par FK; index sur clés étrangères et colonnes de filtrage fréquentes.
- Internationalisation limitée (l’UI est FR/JP/EN) : les libellés d’items linguistiques comportent champs pour’écriture, lecture, gloss.

Schéma relationnel proposé
1) Comptes et profils
- users
  - id (uuid, pk)
  - email (text unique, not null)
  - password_hash (text) — si auth interne; sinon external_provider / external_id
  - display_name (text)
  - avatar_url (text)
  - locale (text, ex: 'fr-FR')
  - timezone (text, ex: 'Europe/Paris')
  - created_at, updated_at
  - last_login_at
- user_settings
  - user_id (uuid pk/fk users)
  - daily_study_goal_minutes (int)
  - weekly_study_goal_minutes (int)
  - srs_prefs (jsonb) — algorithmes, intervalles, modes
  - notifications_prefs (jsonb)
  - premium_until (timestamptz null) — abonnement
- sessions (optionnel si auth par session)
  - id (uuid pk)
  - user_id (uuid fk)
  - created_at, expires_at, ip, user_agent

2) Contenu / Bibliothèque
- works (œuvres)
  - id (uuid pk)
  - title (text)
  - type (enum: book, manga, anime, game, other)
  - author (text)
  - difficulty_level (int null)
  - source_url (text null)
  - metadata (jsonb)
  - created_at, updated_at
- work_segments (pour granularité chapitres/épisodes/pages)
  - id (uuid pk)
  - work_id (uuid fk works)
  - kind (enum: chapter, episode, page_range, scene, other)
  - index_no (int)
  - title (text null)
  - metadata (jsonb)

5) Temps d’étude, sessions, vitesses de lecture
- study_sessions
  - id (uuid pk)
  - user_id (uuid fk users)
  - started_at (timestamptz)
  - ended_at (timestamptz)
  - duration_sec (int, check = ended_at >= started_at)
  - modality (enum: practice, listen, write, speak, review, read)
  - work_id (uuid fk works null) — ex: manga/jeu
  - work_segment_id (uuid fk work_segments null)
  - words_reviewed (int null)
  - words_learned (int null)
  - notes (text null)
- reading_speeds
  - id (uuid pk)
  - user_id (uuid fk users)
  - work_id (uuid fk works)
  - measured_at (timestamptz)
  - chars_per_min (int)
  - method (enum: manual, auto)

6) Activité & feed
- activity_events
  - id (uuid pk)
  - user_id (uuid fk users)
  - occurred_at (timestamptz)
  - type (enum: session_logged, review_completed, achievement_unlocked, goal_reached, media_added, vocabulary_mastered, streak_extended)
  - ref_kind (text) — nature de la référence (work, item, achievement, goal, session)
  - ref_id (uuid null) — identifiant vers la ressource référencée
  - summary (text) — ex: "Read 32 pages of 'Spy x Family'"
  - metadata (jsonb)
  - visibility (enum: private, friends, public) — si social
  - indexes: (user_id, occurred_at desc), (type, occurred_at desc)

7) Réalisations & objectifs
- achievements_catalog
  - id (uuid pk)
  - code (text unique) — ex: KANJI_MASTER_100
  - name (text)
  - description (text)
  - icon (text) — code de glyphe/emoji
  - criteria (jsonb) — règles de déverrouillage
- user_achievements
  - user_id (uuid fk users)
  - achievement_id (uuid fk achievements_catalog)
  - unlocked_at (timestamptz)
  - is_new (bool) — pour badge "New!"
  - pk (user_id, achievement_id)
- goals
  - id (uuid pk)
  - user_id (uuid fk users)
  - period (enum: daily, weekly, monthly)
  - metric (enum: words_learned, study_minutes)
  - target (int)
  - start_date (date) — pour weekly/monthly
  - end_date (date)
  - created_at, updated_at
- goal_progress
  - goal_id (uuid fk goals)
  - measured_at (timestamptz)
  - value (int)
  - pk (goal_id, measured_at)

8) Classements (Leaderboard)
- leaderboards (définition)
  - id (uuid pk)
  - scope (enum: global, friends, local)
  - metric (enum: study_minutes, words_learned, streak_days)
  - period (enum: daily, weekly, monthly, all_time)
  - created_at
- leaderboard_entries (scores matérialisés)
  - leaderboard_id (uuid fk leaderboards)
  - user_id (uuid fk users)
  - score (numeric)
  - rank (int)
  - computed_at (timestamptz)
  - pk (leaderboard_id, user_id)

9) Abonnements (Premium)
- products (si facturation propre)
  - id (uuid pk)
  - code (text unique)
  - name (text)
  - price_cents (int)
  - currency (text)
  - interval (enum: month, year)
- subscriptions
  - id (uuid pk)
  - user_id (uuid fk users)
  - product_id (uuid fk products)
  - status (enum: active, past_due, canceled, trialing)
  - current_period_start, current_period_end
  - external_provider (text), external_sub_id (text)
  - created_at, updated_at

11) Notifications
- notifications
  - id (uuid pk)
  - user_id (uuid fk users)
  - type (enum: achievement, reminder, goal, system)
  - title (text)
  - body (text)
  - created_at (timestamptz)
  - read_at (timestamptz null)


Vues matérialisées / agrégations conseillées
- mv_user_daily_activity (par utilisateur et date)
  - user_id, activity_date (date), study_minutes (int), words_learned (int), sessions_count (int)
  - alimente: heatmap, cartes stats
- mv_user_streaks
  - user_id, current_streak_days, longest_streak_days, updated_at
- mv_media_consumption
  - user_id, type, items_count sur période
- mv_weekly_study_time
  - user_id, week_start (date), minutes_by_weekday (int[7]), total_minutes
- Indexation: créer index sur (user_id, date/occurred_at), et GIN pour jsonb si nécessaire.

Notes d’implémentation
- Types enum: privilégier des enums SQL ou des check constraints + tables de référence (ex: media_type, activity_type) selon préférence de migration.
- Recherche plein‑texte (FTS): vecteurs tsvector sur vocab_items.meanings, example_sentences.jp pour une future "Library" avec recherche.
- Internationalisation: pour meanings multilingues, prévoir vocab_translations(id, vocab_id, lang, meaning, notes).
- Confidentialité: activity_events.visibility pour partager un feed social.
- Performance: privilégier des tables d’historique append‑only (ex. activity_events) et des vues matérialisées pour les agrégations.
- Nettoyage: study_sessions.duration_sec peut être calculé; conserver néanmoins pour requêtes faciles.

Traçabilité UI → modèle
- Stats Cards: mv_user_daily_activity + agrégations sur study_sessions.
- Heatmap: mv_user_daily_activity par date.
- Achievements: achievements_catalog + user_achievements.is_new.
- Goals: goals + goal_progress; cartes affichent la progression actuelle vs target.
- Quick Actions: study_sessions.modality pour logguer les actions.
- Recent Entries: activity_events et/ou study_sessions/works.
- Media Consumption: works.type + activity_events/media_added + agrégation par type.
- Weekly Study Time: study_sessions agrégé en minutes par jour de semaine.
- Reading Speed: reading_speeds par work.
- Activity Feed: activity_events ordonné par occurred_at.
- Leaderboard: leaderboards + leaderboard_entries (matérialisé périodiquement).
- Subscribe: user_settings.premium_until ou subscriptions si intégration PSP.
- Submit: uploads, reliés à works ou analyses futures via metadata.

Sécurité et contraintes
- FK ON DELETE CASCADE ou SET NULL selon cardinalités: ex. suppression user → anonymiser (GDPR) : remplacer par actor_user_id null et conserver activité agrégée.
- Unicité:
  - users.email unique
  - kanji_items.character unique
  - achievements_catalog.code unique
- Index clés:
  - activity_events(user_id, occurred_at desc)
  - study_sessions(user_id, started_at desc)
  - user_achievements(user_id, unlocked_at desc)

Exemples de tables SQL (PostgreSQL) — extraits

-- users
-- create table users (
--   id uuid primary key default gen_random_uuid(),
--   email text unique not null,
--   password_hash text,
--   display_name text,
--   avatar_url text,
--   locale text,
--   timezone text,
--   created_at timestamptz not null default now(),
--   updated_at timestamptz not null default now(),
--   last_login_at timestamptz
-- );

-- activity_events
-- create table activity_events (
--   id uuid primary key default gen_random_uuid(),
--   user_id uuid not null references users(id),
--   occurred_at timestamptz not null default now(),
--   type text not null,
--   ref_kind text,
--   ref_id uuid,
--   summary text,
--   metadata jsonb,
--   visibility text not null default 'private'
-- );
-- create index on activity_events(user_id, occurred_at desc);

Limites et hypothèses
- Pas d’API fournie: le modèle couvre les besoins évidents de l’UI; il sera affiné dès que les règles métier exactes seront posées (ex. calcul du "Words Learned").
- Social/Privacy: les aspects sociaux sont optionnels; le modèle reste utilisable sans.

Prochaines étapes
- Valider les métriques exactes derrière chaque carte (définitions métier).
- Décider du fournisseur d’auth/payment (intégration OAuth, Stripe, etc.).
- Définir les enums/tables de référence finales et les migrations.
- Prototyper les vues matérialisées et tâches de calcul (cron/worker).
- Ébaucher l’API (REST/GraphQL) pour alimenter les pages actuelles.

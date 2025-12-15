--
-- PostgreSQL database dump
--

\restrict Caqv0xe0XYa0fHJKtz9AlntKkMi7e1dAfaC5R1wJzfO9p2SEl4XibZlg7PwvzD6

-- Dumped from database version 17.6 (Homebrew)
-- Dumped by pg_dump version 17.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO dimaeboshi;

--
-- Name: spheres; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.spheres (
    id integer NOT NULL,
    user_id integer,
    name text NOT NULL
);


ALTER TABLE public.spheres OWNER TO dimaeboshi;

--
-- Name: spheres_id_seq; Type: SEQUENCE; Schema: public; Owner: dimaeboshi
--

CREATE SEQUENCE public.spheres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.spheres_id_seq OWNER TO dimaeboshi;

--
-- Name: spheres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dimaeboshi
--

ALTER SEQUENCE public.spheres_id_seq OWNED BY public.spheres.id;


--
-- Name: subtasks; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.subtasks (
    id integer NOT NULL,
    task_id integer,
    title text NOT NULL,
    is_done boolean DEFAULT false
);


ALTER TABLE public.subtasks OWNER TO dimaeboshi;

--
-- Name: subtasks_id_seq; Type: SEQUENCE; Schema: public; Owner: dimaeboshi
--

CREATE SEQUENCE public.subtasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subtasks_id_seq OWNER TO dimaeboshi;

--
-- Name: subtasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dimaeboshi
--

ALTER SEQUENCE public.subtasks_id_seq OWNED BY public.subtasks.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    user_id integer,
    name text NOT NULL
);


ALTER TABLE public.tags OWNER TO dimaeboshi;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: dimaeboshi
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO dimaeboshi;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dimaeboshi
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: task_metrics; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.task_metrics (
    task_id integer NOT NULL,
    l numeric(5,2) NOT NULL,
    v numeric(5,2) NOT NULL,
    d numeric(5,2) NOT NULL,
    e numeric(5,2) NOT NULL,
    re numeric(5,2) NOT NULL
);


ALTER TABLE public.task_metrics OWNER TO dimaeboshi;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    user_id integer,
    tag_id integer,
    sphere_id integer,
    title text NOT NULL,
    description text,
    deadline timestamp without time zone,
    priority numeric(3,1),
    is_done boolean DEFAULT false,
    archived boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT tasks_check CHECK (((archived = false) OR (is_done = true)))
);


ALTER TABLE public.tasks OWNER TO dimaeboshi;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: dimaeboshi
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO dimaeboshi;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dimaeboshi
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dimaeboshi
--

CREATE TABLE public.users (
    id integer NOT NULL,
    telegram_id bigint NOT NULL,
    username text,
    fullname text,
    task_creation_type character varying(20) DEFAULT 'quick'::character varying,
    notifications_enabled boolean DEFAULT false,
    notification_time time without time zone,
    CONSTRAINT users_task_creation_type_check CHECK (((task_creation_type)::text = ANY ((ARRAY['quick'::character varying, 'detailed'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO dimaeboshi;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dimaeboshi
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO dimaeboshi;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dimaeboshi
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: spheres id; Type: DEFAULT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.spheres ALTER COLUMN id SET DEFAULT nextval('public.spheres_id_seq'::regclass);


--
-- Name: subtasks id; Type: DEFAULT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.subtasks ALTER COLUMN id SET DEFAULT nextval('public.subtasks_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.alembic_version (version_num) FROM stdin;
fa31708d8cb7
\.


--
-- Data for Name: spheres; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.spheres (id, user_id, name) FROM stdin;
3	2	Здоровье
4	2	Творчество
5	1	LMAO
6	4	хехе
7	4	Учёба
8	4	У412412
9	4	Учёба
10	4	{F{F{F{{FF
\.


--
-- Data for Name: subtasks; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.subtasks (id, task_id, title, is_done) FROM stdin;
7	4	Наброски	t
2	1	Сделать графики	f
1	1	Собрать данные	f
3	2	Прочитать введение	f
8	4	Окончательная работа	t
4	12	Прочитать весь текст	t
10	12	Новая подзадача	f
11	12	Новая подзадача для теста	f
12	14	Новая подзадача для теста	f
13	14	Новая подзадача для теста	f
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.tags (id, user_id, name) FROM stdin;
3	2	Фитнес
4	2	Хобби
2	1	хехехе
6	1	АБВ
5	1	иди нахуй
7	4	йоооу
8	4	Учёба
9	4	Учёба
10	4	looool
\.


--
-- Data for Name: task_metrics; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.task_metrics (task_id, l, v, d, e, re) FROM stdin;
1	4.00	1.00	3.00	1.00	8.00
10	0.00	0.00	0.00	0.00	0.00
11	0.00	0.00	0.00	0.00	0.00
13	0.00	0.00	0.00	0.00	0.00
12	1.50	10.00	3.00	0.50	1.00
14	0.00	0.00	0.00	0.00	0.00
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.tasks (id, user_id, tag_id, sphere_id, title, description, deadline, priority, is_done, archived, created_at, updated_at) FROM stdin;
2	1	2	\N	Прочитать статью	Прочитать новую научную статью	2025-09-15 12:00:00	5.0	f	f	2025-09-13 15:34:34.812295	2025-09-13 15:34:34.812295
9	1	\N	5	хуй	адлфвыаджлтфывпдф	\N	\N	f	f	2025-09-26 13:40:15.869508	2025-09-30 20:28:42.923648
1	1	\N	\N	Бля	Составить отчёт по проекту	2025-09-20 18:00:00	1.0	t	t	2025-09-13 15:34:34.812295	2025-09-30 20:28:45.146888
10	2	3	4	допустим	243452135	2025-09-30 20:39:00	0.0	t	f	2025-09-30 20:38:35.52928	2025-09-30 20:50:57.916564
11	2	4	4	ТЕСТ	323	2025-09-18 20:51:00	0.0	t	t	2025-09-30 20:51:58.235238	2025-09-30 20:53:13.596603
4	2	\N	\N	fdf	fdafadf	2025-09-18 20:00:00	4.5	t	t	2025-09-13 15:34:34.812295	2025-09-30 21:09:22.59327
13	4	\N	\N	Сделать дз	Написать по информатике	\N	0.0	f	f	2025-10-04 12:59:56.007077	2025-10-04 12:59:56.007077
12	4	7	6	аква	афвыа	2025-10-15 20:21:00	9.9	f	f	2025-10-03 20:21:21.33796	2025-10-06 12:57:00.873508
14	4	7	6	Просроченная задача	Для проверки overdue и фильтров	2025-01-01 12:00:00	0.0	f	f	2025-10-06 13:15:51.865239	2025-10-06 13:15:51.865239
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dimaeboshi
--

COPY public.users (id, telegram_id, username, fullname, task_creation_type, notifications_enabled, notification_time) FROM stdin;
2	987654321	anna_s	Анна Смирнова	quick	t	\N
1	123456789	yeathis	Виктория	quick	t	\N
4	279058397	vdkfrost	Vladislav Kibenko	quick	t	\N
5	100500	ivan_test	Ivan Petrov	quick	t	\N
\.


--
-- Name: spheres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dimaeboshi
--

SELECT pg_catalog.setval('public.spheres_id_seq', 10, true);


--
-- Name: subtasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dimaeboshi
--

SELECT pg_catalog.setval('public.subtasks_id_seq', 13, true);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dimaeboshi
--

SELECT pg_catalog.setval('public.tags_id_seq', 10, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dimaeboshi
--

SELECT pg_catalog.setval('public.tasks_id_seq', 14, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dimaeboshi
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: spheres spheres_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.spheres
    ADD CONSTRAINT spheres_pkey PRIMARY KEY (id);


--
-- Name: subtasks subtasks_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.subtasks
    ADD CONSTRAINT subtasks_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: task_metrics task_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.task_metrics
    ADD CONSTRAINT task_metrics_pkey PRIMARY KEY (task_id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_telegram_id_key; Type: CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_id_key UNIQUE (telegram_id);


--
-- Name: spheres spheres_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.spheres
    ADD CONSTRAINT spheres_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: subtasks subtasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.subtasks
    ADD CONSTRAINT subtasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- Name: tags tags_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: task_metrics task_metrics_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.task_metrics
    ADD CONSTRAINT task_metrics_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- Name: tasks tasks_sphere_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_sphere_id_fkey FOREIGN KEY (sphere_id) REFERENCES public.spheres(id) ON DELETE SET NULL;


--
-- Name: tasks tasks_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE SET NULL;


--
-- Name: tasks tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dimaeboshi
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Caqv0xe0XYa0fHJKtz9AlntKkMi7e1dAfaC5R1wJzfO9p2SEl4XibZlg7PwvzD6


--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: codes; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.codes (
    id integer NOT NULL,
    reset_code integer NOT NULL,
    own integer NOT NULL
);


ALTER TABLE public.codes OWNER TO edwardhuang;

--
-- Name: codes_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.codes_id_seq OWNER TO edwardhuang;

--
-- Name: codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.codes_id_seq OWNED BY public.codes.id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    comment text NOT NULL,
    has integer NOT NULL,
    owns integer NOT NULL
);


ALTER TABLE public.comments OWNER TO edwardhuang;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_comment_id_seq OWNER TO edwardhuang;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: cookbooks; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.cookbooks (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    contains integer NOT NULL
);


ALTER TABLE public.cookbooks OWNER TO edwardhuang;

--
-- Name: cookbooks_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.cookbooks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cookbooks_id_seq OWNER TO edwardhuang;

--
-- Name: cookbooks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.cookbooks_id_seq OWNED BY public.cookbooks.id;


--
-- Name: cookbooks_lists; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.cookbooks_lists (
    id integer NOT NULL,
    cookbook_id integer NOT NULL,
    recipe_id integer NOT NULL
);


ALTER TABLE public.cookbooks_lists OWNER TO edwardhuang;

--
-- Name: cookbooks_lists_cookbook_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.cookbooks_lists_cookbook_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cookbooks_lists_cookbook_id_seq OWNER TO edwardhuang;

--
-- Name: cookbooks_lists_cookbook_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.cookbooks_lists_cookbook_id_seq OWNED BY public.cookbooks_lists.cookbook_id;


--
-- Name: cookbooks_lists_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.cookbooks_lists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cookbooks_lists_id_seq OWNER TO edwardhuang;

--
-- Name: cookbooks_lists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.cookbooks_lists_id_seq OWNED BY public.cookbooks_lists.id;


--
-- Name: history; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.history (
    id integer NOT NULL,
    userid integer NOT NULL,
    recipe integer NOT NULL,
    last_view_time time without time zone DEFAULT date_trunc('second'::text, (LOCALTIME)::interval),
    last_view_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.history OWNER TO edwardhuang;

--
-- Name: history_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.history_id_seq OWNER TO edwardhuang;

--
-- Name: history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.history_id_seq OWNED BY public.history.id;


--
-- Name: ingredient; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.ingredient (
    id integer NOT NULL,
    recipe_id integer,
    ingredient text,
    dosage double precision,
    unit_name text
);


ALTER TABLE public.ingredient OWNER TO edwardhuang;

--
-- Name: ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.ingredient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredient_id_seq OWNER TO edwardhuang;

--
-- Name: ingredient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.ingredient_id_seq OWNED BY public.ingredient.id;


--
-- Name: likes; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.likes (
    id integer NOT NULL,
    like_status integer NOT NULL,
    has integer NOT NULL,
    own integer NOT NULL
);


ALTER TABLE public.likes OWNER TO edwardhuang;

--
-- Name: likes_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.likes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.likes_id_seq OWNER TO edwardhuang;

--
-- Name: likes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.likes_id_seq OWNED BY public.likes.id;


--
-- Name: method; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.method (
    recipe_id integer NOT NULL,
    method text NOT NULL
);


ALTER TABLE public.method OWNER TO edwardhuang;

--
-- Name: profiles; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.profiles (
    profile_id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    display_name text NOT NULL,
    profile_pic text NOT NULL,
    temp_pic text,
    bio text,
    custom_url text,
    owns integer NOT NULL,
    sub_count integer DEFAULT 0,
    recipe_count integer DEFAULT 0
);


ALTER TABLE public.profiles OWNER TO edwardhuang;

--
-- Name: recipes; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.recipes (
    id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    photo text,
    serving integer NOT NULL,
    num_of_likes integer DEFAULT 0,
    num_of_dislikes integer DEFAULT 0,
    creates integer NOT NULL,
    creator text NOT NULL,
    meal_type text NOT NULL,
    creation_time time without time zone DEFAULT date_trunc('second'::text, (LOCALTIME)::interval),
    creation_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.recipes OWNER TO edwardhuang;

--
-- Name: subscribed; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.subscribed (
    subscribed_id integer NOT NULL,
    contains integer NOT NULL
);


ALTER TABLE public.subscribed OWNER TO edwardhuang;

--
-- Name: newsfeeds; Type: VIEW; Schema: public; Owner: edwardhuang
--

CREATE VIEW public.newsfeeds AS
 SELECT r.id,
    r.name,
    r.description,
    r.photo,
    r.serving,
    r.creates,
    r.creator,
    s.contains,
    r.num_of_likes AS likes,
    r.num_of_dislikes AS dislikes,
    p.display_name,
    r.creation_time,
    r.creation_date
   FROM ((public.recipes r
     JOIN public.subscribed s ON ((r.creates = s.subscribed_id)))
     JOIN public.profiles p ON ((r.creates = p.profile_id)));


ALTER TABLE public.newsfeeds OWNER TO edwardhuang;

--
-- Name: newsletters; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.newsletters (
    id integer NOT NULL,
    subscribed_to boolean NOT NULL,
    own integer NOT NULL
);


ALTER TABLE public.newsletters OWNER TO edwardhuang;

--
-- Name: newsletters_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.newsletters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.newsletters_id_seq OWNER TO edwardhuang;

--
-- Name: newsletters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.newsletters_id_seq OWNED BY public.newsletters.id;


--
-- Name: profile_subbed; Type: VIEW; Schema: public; Owner: edwardhuang
--

CREATE VIEW public.profile_subbed AS
 SELECT p.profile_id,
    p.first_name,
    p.last_name,
    p.display_name,
    p.profile_pic,
    p.bio,
    p.custom_url,
    p.sub_count,
    p.recipe_count,
    s.subscribed_id,
    s.contains
   FROM (public.profiles p
     LEFT JOIN public.subscribed s ON ((p.profile_id = s.subscribed_id)));


ALTER TABLE public.profile_subbed OWNER TO edwardhuang;

--
-- Name: subscriber; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.subscriber (
    subscriber_id integer NOT NULL,
    contains integer NOT NULL
);


ALTER TABLE public.subscriber OWNER TO edwardhuang;

--
-- Name: profile_subs; Type: VIEW; Schema: public; Owner: edwardhuang
--

CREATE VIEW public.profile_subs AS
 SELECT p.profile_id,
    p.first_name,
    p.last_name,
    p.display_name,
    p.profile_pic,
    p.bio,
    p.custom_url,
    p.sub_count,
    p.recipe_count,
    s.subscriber_id,
    s.contains
   FROM (public.profiles p
     LEFT JOIN public.subscriber s ON ((p.profile_id = s.subscriber_id)));


ALTER TABLE public.profile_subs OWNER TO edwardhuang;

--
-- Name: profiles_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.profiles_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.profiles_profile_id_seq OWNER TO edwardhuang;

--
-- Name: profiles_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.profiles_profile_id_seq OWNED BY public.profiles.profile_id;


--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_id_seq OWNER TO edwardhuang;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: recipestep; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.recipestep (
    recipe_id integer NOT NULL,
    step_no integer NOT NULL,
    step_comment text NOT NULL,
    photo text
);


ALTER TABLE public.recipestep OWNER TO edwardhuang;

--
-- Name: starred_recipes; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.starred_recipes (
    recipe_id integer NOT NULL,
    contains integer NOT NULL
);


ALTER TABLE public.starred_recipes OWNER TO edwardhuang;

--
-- Name: users; Type: TABLE; Schema: public; Owner: edwardhuang
--

CREATE TABLE public.users (
    id integer NOT NULL,
    password text NOT NULL,
    email text NOT NULL,
    CONSTRAINT users_email_check CHECK ((email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'::text)),
    CONSTRAINT users_password_check CHECK ((length(password) > 5))
);


ALTER TABLE public.users OWNER TO edwardhuang;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: edwardhuang
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO edwardhuang;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edwardhuang
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: codes id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.codes ALTER COLUMN id SET DEFAULT nextval('public.codes_id_seq'::regclass);


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: cookbooks id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks ALTER COLUMN id SET DEFAULT nextval('public.cookbooks_id_seq'::regclass);


--
-- Name: cookbooks_lists id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks_lists ALTER COLUMN id SET DEFAULT nextval('public.cookbooks_lists_id_seq'::regclass);


--
-- Name: cookbooks_lists cookbook_id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks_lists ALTER COLUMN cookbook_id SET DEFAULT nextval('public.cookbooks_lists_cookbook_id_seq'::regclass);


--
-- Name: history id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.history ALTER COLUMN id SET DEFAULT nextval('public.history_id_seq'::regclass);


--
-- Name: ingredient id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.ingredient ALTER COLUMN id SET DEFAULT nextval('public.ingredient_id_seq'::regclass);


--
-- Name: likes id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.likes ALTER COLUMN id SET DEFAULT nextval('public.likes_id_seq'::regclass);


--
-- Name: newsletters id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.newsletters ALTER COLUMN id SET DEFAULT nextval('public.newsletters_id_seq'::regclass);


--
-- Name: profiles profile_id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.profiles ALTER COLUMN profile_id SET DEFAULT nextval('public.profiles_profile_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: codes; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.codes (id, reset_code, own) FROM stdin;
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.comments (comment_id, comment, has, owns) FROM stdin;
\.


--
-- Data for Name: cookbooks; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.cookbooks (id, name, description, contains) FROM stdin;
1	NewBook	\N	1
2	NewBook1	\N	1
\.


--
-- Data for Name: cookbooks_lists; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.cookbooks_lists (id, cookbook_id, recipe_id) FROM stdin;
1	2	1
\.


--
-- Data for Name: history; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.history (id, userid, recipe, last_view_time, last_view_date) FROM stdin;
2	2	1	16:39:38.711199	2021-08-02
1	1	1	16:43:25.759542	2021-08-02
\.


--
-- Data for Name: ingredient; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.ingredient (id, recipe_id, ingredient, dosage, unit_name) FROM stdin;
1	1	pork	1	g
2	1	beef	1	cups
3	1	salt	1	ml
\.


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.likes (id, like_status, has, own) FROM stdin;
1	1	1	1
\.


--
-- Data for Name: method; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.method (recipe_id, method) FROM stdin;
1	Grilling
1	Steaming
\.


--
-- Data for Name: newsletters; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.newsletters (id, subscribed_to, own) FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.profiles (profile_id, first_name, last_name, display_name, profile_pic, temp_pic, bio, custom_url, owns, sub_count, recipe_count) FROM stdin;
1	Edward	Huang	Edward Huang	default_user.jpg	\N	Not much is known about this user... Encourage them to setup their user bio!	1	1	\N	0
2	Ziqiu	Huang	Ziqiu Huang	default_user.jpg	\N	Not much is known about this user... Encourage them to setup their user bio!	2	2	\N	0
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.recipes (id, name, description, photo, serving, num_of_likes, num_of_dislikes, creates, creator, meal_type, creation_time, creation_date) FROM stdin;
1	sushi	sushi is good	sushi-header-blog.jpeg	2	1	0	1	Edward Huang	Main	16:12:33	2021-08-02
\.


--
-- Data for Name: recipestep; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.recipestep (recipe_id, step_no, step_comment, photo) FROM stdin;
1	1	Xcode is an Integrated Development Environment, which means it pulls all the tools needed to produce an application (particularly a text editor, a compiler, and a build system) into one software package rather than leaving them as a set of individual tools connected by scripts. Xcode is Apple's official IDE for Mac and iOS developers; it was originally known as Project Builder in the NeXT days, and renamed to Xcode somewhere around Mac OS X 10.3 or 10.4. By version 4, Apple had folded in the companion Interface Builder program so there was only one app bundle; the design of the program hasn't changed a whole lot since then, although obviously the tools are updated regularly.	how-to-eat-sushi-1458298_FINAL-5c11371846e0fb0001740595.png
1	2	The next question is "Why do I need it?" (More like "Why do I need it if I'm not a programmer?") Well, there's a couple of uses for it that don't involve writing your own code. One is to sideload programs onto iOS 9 or later using Xcode 7 or later; you need the source code and a cryptographic signature to do this, so you can't just arbitrarily upload any iOS program like you could with a jailbreak, but it's possible, if a little complicated. This is a new feature in Xcode 7 and I think it mainly exists to encourage younger programmers to design their own programs without having to pony up for the Apple Developer program; being able to sideload is just gravy.	sicilian-pasta.jpeg
1	3	Beyond all that, you'll probably want it for doing Hour of Code if you wish to participate in that, although there are simpler options like Qt Creator that won't be quite as intimidating to a beginner. If you're learning Swift, though, the playground feature is really nice, not too far off from coding in a scripting language with immediate execution rather than waiting for an entire project to build.	fresh-salmon-sushi-rolls.jpeg
\.


--
-- Data for Name: starred_recipes; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.starred_recipes (recipe_id, contains) FROM stdin;
\.


--
-- Data for Name: subscribed; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.subscribed (subscribed_id, contains) FROM stdin;
\.


--
-- Data for Name: subscriber; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.subscriber (subscriber_id, contains) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: edwardhuang
--

COPY public.users (id, password, email) FROM stdin;
1	sha256$0WhhejrB$743a9b0df9cc542b217e0de75dd4d0c642cb681caf3953c5e9f9bd75d86e1ec0	thefirsthuang@gmail.com
2	sha256$HGt41Z26$3658af6ccaf8753b439d895c2b3f3620a6bae72e1b10854d5c58c1fc1c183d72	996831033@qq.com
\.


--
-- Name: codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.codes_id_seq', 1, false);


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 1, false);


--
-- Name: cookbooks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.cookbooks_id_seq', 2, true);


--
-- Name: cookbooks_lists_cookbook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.cookbooks_lists_cookbook_id_seq', 1, false);


--
-- Name: cookbooks_lists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.cookbooks_lists_id_seq', 1, true);


--
-- Name: history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.history_id_seq', 2, true);


--
-- Name: ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.ingredient_id_seq', 3, true);


--
-- Name: likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.likes_id_seq', 1, true);


--
-- Name: newsletters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.newsletters_id_seq', 1, false);


--
-- Name: profiles_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.profiles_profile_id_seq', 2, true);


--
-- Name: recipes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.recipes_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edwardhuang
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: codes codes_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.codes
    ADD CONSTRAINT codes_pkey PRIMARY KEY (id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: cookbooks cookbooks_id_key; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks
    ADD CONSTRAINT cookbooks_id_key UNIQUE (id);


--
-- Name: cookbooks_lists cookbooks_lists_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks_lists
    ADD CONSTRAINT cookbooks_lists_pkey PRIMARY KEY (id);


--
-- Name: cookbooks cookbooks_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks
    ADD CONSTRAINT cookbooks_pkey PRIMARY KEY (id, contains);


--
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_pkey PRIMARY KEY (id);


--
-- Name: ingredient ingredient_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.ingredient
    ADD CONSTRAINT ingredient_pkey PRIMARY KEY (id);


--
-- Name: likes likes_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (id);


--
-- Name: method method_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.method
    ADD CONSTRAINT method_pkey PRIMARY KEY (recipe_id, method);


--
-- Name: newsletters newsletters_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.newsletters
    ADD CONSTRAINT newsletters_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (profile_id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: recipestep recipestep_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.recipestep
    ADD CONSTRAINT recipestep_pkey PRIMARY KEY (recipe_id, step_no);


--
-- Name: starred_recipes starred_recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.starred_recipes
    ADD CONSTRAINT starred_recipes_pkey PRIMARY KEY (recipe_id, contains);


--
-- Name: subscribed subscribed_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.subscribed
    ADD CONSTRAINT subscribed_pkey PRIMARY KEY (subscribed_id, contains);


--
-- Name: subscriber subscriber_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.subscriber
    ADD CONSTRAINT subscriber_pkey PRIMARY KEY (subscriber_id, contains);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: codes codes_own_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.codes
    ADD CONSTRAINT codes_own_fkey FOREIGN KEY (own) REFERENCES public.users(id);


--
-- Name: comments comments_has_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_has_fkey FOREIGN KEY (has) REFERENCES public.recipes(id);


--
-- Name: comments comments_owns_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_owns_fkey FOREIGN KEY (owns) REFERENCES public.users(id);


--
-- Name: cookbooks cookbooks_contains_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks
    ADD CONSTRAINT cookbooks_contains_fkey FOREIGN KEY (contains) REFERENCES public.users(id);


--
-- Name: cookbooks_lists cookbooks_lists_cookbook_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks_lists
    ADD CONSTRAINT cookbooks_lists_cookbook_id_fkey FOREIGN KEY (cookbook_id) REFERENCES public.cookbooks(id);


--
-- Name: cookbooks_lists cookbooks_lists_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.cookbooks_lists
    ADD CONSTRAINT cookbooks_lists_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: history history_recipe_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_recipe_fkey FOREIGN KEY (recipe) REFERENCES public.recipes(id);


--
-- Name: history history_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(id);


--
-- Name: ingredient ingredient_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.ingredient
    ADD CONSTRAINT ingredient_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: likes likes_has_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_has_fkey FOREIGN KEY (has) REFERENCES public.recipes(id);


--
-- Name: likes likes_own_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_own_fkey FOREIGN KEY (own) REFERENCES public.users(id);


--
-- Name: method method_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.method
    ADD CONSTRAINT method_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: newsletters newsletters_own_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.newsletters
    ADD CONSTRAINT newsletters_own_fkey FOREIGN KEY (own) REFERENCES public.users(id);


--
-- Name: profiles profiles_owns_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_owns_fkey FOREIGN KEY (owns) REFERENCES public.users(id);


--
-- Name: recipes recipes_creates_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_creates_fkey FOREIGN KEY (creates) REFERENCES public.users(id);


--
-- Name: recipestep recipestep_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.recipestep
    ADD CONSTRAINT recipestep_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: starred_recipes starred_recipes_contains_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.starred_recipes
    ADD CONSTRAINT starred_recipes_contains_fkey FOREIGN KEY (contains) REFERENCES public.profiles(profile_id);


--
-- Name: starred_recipes starred_recipes_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.starred_recipes
    ADD CONSTRAINT starred_recipes_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(id);


--
-- Name: subscribed subscribed_contains_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.subscribed
    ADD CONSTRAINT subscribed_contains_fkey FOREIGN KEY (contains) REFERENCES public.profiles(profile_id);


--
-- Name: subscriber subscriber_contains_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edwardhuang
--

ALTER TABLE ONLY public.subscriber
    ADD CONSTRAINT subscriber_contains_fkey FOREIGN KEY (contains) REFERENCES public.profiles(profile_id);


--
-- PostgreSQL database dump complete
--


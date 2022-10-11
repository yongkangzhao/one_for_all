import psycopg

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg.connect("dbname=postgres user=postgres password=postgres host=localhost port=5432")
        return conn
    except:
        print("Unable to connect to the database")


def create_project():
    """
    CREATE TABLE IF NOT EXISTS public.projects_project
    (
        id integer NOT NULL DEFAULT nextval('api_project_id_seq'::regclass),
        name character varying(100) COLLATE pg_catalog."default" NOT NULL,
        description text COLLATE pg_catalog."default" NOT NULL,
        guideline text COLLATE pg_catalog."default" NOT NULL,
        created_at timestamp with time zone NOT NULL,
        updated_at timestamp with time zone NOT NULL,
        project_type character varying(30) COLLATE pg_catalog."default" NOT NULL,
        random_order boolean NOT NULL,
        collaborative_annotation boolean NOT NULL,
        polymorphic_ctype_id integer,
        single_class_classification boolean NOT NULL,
        created_by_id integer,
        CONSTRAINT api_project_pkey PRIMARY KEY (id),
        CONSTRAINT api_project_created_by_id_a4943add_fk_auth_user_id FOREIGN KEY (created_by_id)
            REFERENCES public.auth_user (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            DEFERRABLE INITIALLY DEFERRED,
        CONSTRAINT api_project_polymorphic_ctype_id_a07fc605_fk_django_co FOREIGN KEY (polymorphic_ctype_id)
            REFERENCES public.django_content_type (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            DEFERRABLE INITIALLY DEFERRED
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.projects_project
        OWNER to postgres;
    -- Index: api_project_created_by_id_a4943add

    -- DROP INDEX IF EXISTS public.api_project_created_by_id_a4943add;

    CREATE INDEX IF NOT EXISTS api_project_created_by_id_a4943add
        ON public.projects_project USING btree
        (created_by_id ASC NULLS LAST)
        TABLESPACE pg_default;
    -- Index: api_project_polymorphic_ctype_id_a07fc605

    -- DROP INDEX IF EXISTS public.api_project_polymorphic_ctype_id_a07fc605;

    CREATE INDEX IF NOT EXISTS api_project_polymorphic_ctype_id_a07fc605
        ON public.projects_project USING btree
        (polymorphic_ctype_id ASC NULLS LAST)
        TABLESPACE pg_default;

    CREATE TABLE IF NOT EXISTS public.projects_member
(
    id integer NOT NULL DEFAULT nextval('api_rolemapping_id_seq'::regclass),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    project_id integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT api_rolemapping_pkey PRIMARY KEY (id),
    CONSTRAINT api_rolemapping_user_id_project_id_ba4b621e_uniq UNIQUE (user_id, project_id),
    CONSTRAINT api_rolemapping_project_id_3e054aae_fk_api_project_id FOREIGN KEY (project_id)
        REFERENCES public.projects_project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_rolemapping_role_id_7917de50_fk_api_role_id FOREIGN KEY (role_id)
        REFERENCES public.roles_role (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_rolemapping_user_id_002ab82b_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.projects_member
        OWNER to postgres;
    -- Index: api_rolemapping_project_id_3e054aae

    -- DROP INDEX IF EXISTS public.api_rolemapping_project_id_3e054aae;

    CREATE INDEX IF NOT EXISTS api_rolemapping_project_id_3e054aae
        ON public.projects_member USING btree
        (project_id ASC NULLS LAST)
        TABLESPACE pg_default;
    -- Index: api_rolemapping_role_id_7917de50

    -- DROP INDEX IF EXISTS public.api_rolemapping_role_id_7917de50;

    CREATE INDEX IF NOT EXISTS api_rolemapping_role_id_7917de50
        ON public.projects_member USING btree
        (role_id ASC NULLS LAST)
        TABLESPACE pg_default;
    -- Index: api_rolemapping_user_id_002ab82b

    -- DROP INDEX IF EXISTS public.api_rolemapping_user_id_002ab82b;

    CREATE INDEX IF NOT EXISTS api_rolemapping_user_id_002ab82b
        ON public.projects_member USING btree
        (user_id ASC NULLS LAST)
        TABLESPACE pg_default;
    """
    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO projects_project (name, description, guideline, created_at, updated_at, project_type, random_order, collaborative_annotation, polymorphic_ctype_id, single_class_classification, created_by_id) VALUES ('triple classification', 'classification of triple quality', '', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'DocumentClassification', 'true', 'true', '15', 'true', '1') ON CONFLICT DO NOTHING;")
    triple_classification_id = cur.execute("SELECT id FROM projects_project WHERE name = 'triple classification';").fetchone()[0]
    cur.execute("INSERT INTO projects_member (created_at, updated_at, project_id, role_id, user_id) VALUES ('2019-01-01 00:00:00', '2019-01-01 00:00:00', %s, '1', '1') ON CONFLICT DO NOTHING;", (triple_classification_id,))
    cur.execute("INSERT INTO projects_textclassificationproject (project_ptr_id) VALUES (%s) ON CONFLICT DO NOTHING;", (triple_classification_id,))

    cur.execute("INSERT INTO projects_project (name, description, guideline, created_at, updated_at, project_type, random_order, collaborative_annotation, polymorphic_ctype_id, single_class_classification, created_by_id) VALUES ('sentence classification', 'classification of sentence quality', '', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'DocumentClassification', 'true', 'true', '15', 'true', '1') ON CONFLICT DO NOTHING ;")
    sentence_classification_id = cur.execute("SELECT id FROM projects_project WHERE name = 'sentence classification';").fetchone()[0]
    cur.execute("INSERT INTO projects_member (created_at, updated_at, project_id, role_id, user_id) VALUES ('2019-01-01 00:00:00', '2019-01-01 00:00:00', %s, '1', '1') ON CONFLICT DO NOTHING;", (sentence_classification_id,))
    cur.execute("INSERT INTO projects_textclassificationproject (project_ptr_id) VALUES (%s) ON CONFLICT DO NOTHING;", (sentence_classification_id,))

    conn.commit()

def add_features_to_example():
    conn = connect()
    cur = conn.cursor()
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS head_type TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS head TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS relation TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS tail_type TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS tail TEXT;")
    conn.commit()

def make_project_name_unique():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE projects_project ADD CONSTRAINT unique_name UNIQUE (name);")
    except Exception as e:
        if "already exists" in str(e):
            pass
        else:
            raise e
    conn.commit()

def main():
    make_project_name_unique()
    create_project()
    add_features_to_example()

if __name__ == '__main__':
    main()
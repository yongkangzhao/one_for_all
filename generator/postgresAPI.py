import psycopg
import datetime
import uuid
import json
"""    
CREATE TABLE IF NOT EXISTS public.examples_example
(
    id integer NOT NULL DEFAULT nextval('api_example_id_seq'::regclass),
    meta jsonb NOT NULL,
    filename character varying(1024) COLLATE pg_catalog."default" NOT NULL,
    text text COLLATE pg_catalog."default",
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    annotations_approved_by_id integer,
    project_id integer NOT NULL,
    uuid uuid NOT NULL,
    upload_name character varying(512) COLLATE pg_catalog."default" NOT NULL,
    head_type text COLLATE pg_catalog."default",
    head text COLLATE pg_catalog."default",
    relation text COLLATE pg_catalog."default",
    tail_type text COLLATE pg_catalog."default",
    tail text COLLATE pg_catalog."default",
    entity_type text COLLATE pg_catalog."default",
    CONSTRAINT api_example_pkey PRIMARY KEY (id),
    CONSTRAINT api_example_uuid_52b2ec95_uniq UNIQUE (uuid),
    CONSTRAINT api_example_annotations_approved_by_id_77aff654_fk_auth_user_id FOREIGN KEY (annotations_approved_by_id)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_example_project_id_49dcba10_fk_api_project_id FOREIGN KEY (project_id)
        REFERENCES public.projects_project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.examples_example
    OWNER to postgres;
-- Index: api_example_annotations_approved_by_id_77aff654

-- DROP INDEX IF EXISTS public.api_example_annotations_approved_by_id_77aff654;

CREATE INDEX IF NOT EXISTS api_example_annotations_approved_by_id_77aff654
    ON public.examples_example USING btree
    (annotations_approved_by_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_example_created_at_1e567cc9

-- DROP INDEX IF EXISTS public.api_example_created_at_1e567cc9;

CREATE INDEX IF NOT EXISTS api_example_created_at_1e567cc9
    ON public.examples_example USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_example_project_id_49dcba10

-- DROP INDEX IF EXISTS public.api_example_project_id_49dcba10;

CREATE INDEX IF NOT EXISTS api_example_project_id_49dcba10
    ON public.examples_example USING btree
    (project_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_entity_type_idx

-- DROP INDEX IF EXISTS public.examples_example_entity_type_idx;

CREATE INDEX IF NOT EXISTS examples_example_entity_type_idx
    ON public.examples_example USING btree
    (entity_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_entity_type_text_idx

-- DROP INDEX IF EXISTS public.examples_example_entity_type_text_idx;

CREATE UNIQUE INDEX IF NOT EXISTS examples_example_entity_type_text_idx
    ON public.examples_example USING btree
    (entity_type COLLATE pg_catalog."default" ASC NULLS LAST, text COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_head_idx

-- DROP INDEX IF EXISTS public.examples_example_head_idx;

CREATE INDEX IF NOT EXISTS examples_example_head_idx
    ON public.examples_example USING btree
    (head COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_head_type_head_idx

-- DROP INDEX IF EXISTS public.examples_example_head_type_head_idx;

CREATE INDEX IF NOT EXISTS examples_example_head_type_head_idx
    ON public.examples_example USING btree
    (head_type COLLATE pg_catalog."default" ASC NULLS LAST, head COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_head_type_idx

-- DROP INDEX IF EXISTS public.examples_example_head_type_idx;

CREATE INDEX IF NOT EXISTS examples_example_head_type_idx
    ON public.examples_example USING btree
    (head_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_head_type_relation_tail_type_tail_entity_type_

-- DROP INDEX IF EXISTS public.examples_example_head_type_relation_tail_type_tail_entity_type_;

CREATE INDEX IF NOT EXISTS examples_example_head_type_relation_tail_type_tail_entity_type_
    ON public.examples_example USING btree
    (head_type COLLATE pg_catalog."default" ASC NULLS LAST, relation COLLATE pg_catalog."default" ASC NULLS LAST, tail_type COLLATE pg_catalog."default" ASC NULLS LAST, tail COLLATE pg_catalog."default" ASC NULLS LAST, entity_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_head_type_relation_tail_type_tail_idx

-- DROP INDEX IF EXISTS public.examples_example_head_type_relation_tail_type_tail_idx;

CREATE INDEX IF NOT EXISTS examples_example_head_type_relation_tail_type_tail_idx
    ON public.examples_example USING btree
    (head_type COLLATE pg_catalog."default" ASC NULLS LAST, relation COLLATE pg_catalog."default" ASC NULLS LAST, tail_type COLLATE pg_catalog."default" ASC NULLS LAST, tail COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_relation_idx

-- DROP INDEX IF EXISTS public.examples_example_relation_idx;

CREATE INDEX IF NOT EXISTS examples_example_relation_idx
    ON public.examples_example USING btree
    (relation COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_relation_tail_type_tail_idx

-- DROP INDEX IF EXISTS public.examples_example_relation_tail_type_tail_idx;

CREATE INDEX IF NOT EXISTS examples_example_relation_tail_type_tail_idx
    ON public.examples_example USING btree
    (relation COLLATE pg_catalog."default" ASC NULLS LAST, tail_type COLLATE pg_catalog."default" ASC NULLS LAST, tail COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_tail_idx

-- DROP INDEX IF EXISTS public.examples_example_tail_idx;

CREATE INDEX IF NOT EXISTS examples_example_tail_idx
    ON public.examples_example USING btree
    (tail COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: examples_example_tail_type_idx

-- DROP INDEX IF EXISTS public.examples_example_tail_type_idx;

CREATE INDEX IF NOT EXISTS examples_example_tail_type_idx
    ON public.examples_example USING btree
    (tail_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
"""

class PostgresAPI:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    
    def get_limited_entities(self, entity_type, limit):
        cur = self.conn.cursor()
        # cur.execute("SELECT A.text FROM examples_example AS A JOIN labels_category AS B ON A.id=B.example_id JOIN label_types_categorytype AS C ON B.label_id = C.id")
        # cur.execute("SELECT value FROM examples_example JOIN labels_category JOIN label_types_categorytype WHERE entity_type="+entity_type+" AND label_types_categorytype.text=Positive ORDER BY RANDOM() LIMIT "+str(limit))
        cur.execute("SELECT text FROM examples_example WHERE id IN (SELECT example_id FROM labels_category WHERE label_id IN (SELECT id FROM label_types_categorytype WHERE entity_type = %s)) ORDER BY RANDOM() LIMIT %s", (entity_type, limit))
        rows = cur.fetchall()
        print(rows)
        return [e[0] for e in rows]

    def upsert_entity(self, entity_type, entity, prompt):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT examples_example.meta FROM examples_example WHERE examples_example.entity_type = %s AND examples_example.text = %s", (entity_type, entity))
            count = cur.fetchone()[0][prompt]
        except:
            count = 1
        cur.execute("INSERT INTO examples_example (meta, filename, text, created_at, updated_at, project_id, uuid, upload_name, entity_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (entity_type, text) DO UPDATE SET meta = examples_example.meta || %s", (json.dumps({"entity_type":entity_type,prompt:count+1}), entity, entity, datetime.datetime.now(), datetime.datetime.now(), 1, uuid.uuid1(), entity_type, entity_type, json.dumps({prompt:count+1})))
        self.conn.commit()

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

"""
-- Table: public.prompt_template

-- DROP TABLE IF EXISTS public.prompt_template;

CREATE TABLE IF NOT EXISTS public.prompt_template
(
    id integer NOT NULL DEFAULT nextval('prompt_template_id_seq'::regclass),
    prompt_template_text text COLLATE pg_catalog."default",
    target_entity_type text COLLATE pg_catalog."default",
    CONSTRAINT prompt_template_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.prompt_template
    OWNER to postgres;
-- Index: prompt_template_id_idx

-- DROP INDEX IF EXISTS public.prompt_template_id_idx;

CREATE INDEX IF NOT EXISTS prompt_template_id_idx
    ON public.prompt_template USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: prompt_template_text_idx

-- DROP INDEX IF EXISTS public.prompt_template_text_idx;

CREATE INDEX IF NOT EXISTS prompt_template_text_idx
    ON public.prompt_template USING btree
    (prompt_template_text COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.prompt_instance

-- DROP TABLE IF EXISTS public.prompt_instance;

CREATE TABLE IF NOT EXISTS public.prompt_instance
(
    id integer NOT NULL DEFAULT nextval('prompt_instance_id_seq'::regclass),
    prompt_template_id integer,
    prompt_instance_text text COLLATE pg_catalog."default",
    count integer,
    CONSTRAINT prompt_instance_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.prompt_instance
    OWNER to postgres;
-- Index: prompt_instance_id_idx

-- DROP INDEX IF EXISTS public.prompt_instance_id_idx;

CREATE INDEX IF NOT EXISTS prompt_instance_id_idx
    ON public.prompt_instance USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: prompt_instance_text_idx

-- DROP INDEX IF EXISTS public.prompt_instance_text_idx;

CREATE INDEX IF NOT EXISTS prompt_instance_text_idx
    ON public.prompt_instance USING btree
    (prompt_instance_text COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Table: public.prompt_example

-- DROP TABLE IF EXISTS public.prompt_example;

CREATE TABLE IF NOT EXISTS public.prompt_example
(
    id integer NOT NULL DEFAULT nextval('prompt_example_id_seq'::regclass),
    prompt_instance_id integer,
    example_id integer,
    count integer,
    CONSTRAINT prompt_example_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.prompt_example
    OWNER to postgres;
-- Index: prompt_example_id_idx

-- DROP INDEX IF EXISTS public.prompt_example_id_idx;

CREATE INDEX IF NOT EXISTS prompt_example_id_idx
    ON public.prompt_example USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: prompt_instance_id_example_id_idx

-- DROP INDEX IF EXISTS public.prompt_instance_id_example_id_idx;

CREATE INDEX IF NOT EXISTS prompt_instance_id_example_id_idx
    ON public.prompt_example USING btree
    (prompt_instance_id ASC NULLS LAST, example_id ASC NULLS LAST)
    TABLESPACE pg_default;

"""

"""
-- Table: public.examples_example

-- DROP TABLE IF EXISTS public.examples_example;

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

    def upsert_entity(self, entity_type, entity, prompt_template, prompt_instance):
        cur = self.conn.cursor()
        # get prompt template id
        cur.execute("SELECT id FROM prompt_template WHERE prompt_template_text=%s AND target_entity_type=%s", (prompt_template, entity_type))
        prompt_template_id = cur.fetchone()
        if prompt_template_id is None:
            cur.execute("INSERT INTO prompt_template (prompt_template_text, target_entity_type) VALUES (%s, %s) RETURNING id", (prompt_template, entity_type))
            prompt_template_id = cur.fetchone()[0]
        else:
            prompt_template_id = prompt_template_id[0]
        # get prompt instance id
        cur.execute("SELECT id FROM prompt_instance WHERE prompt_template_id=%s AND prompt_instance_text=%s", (prompt_template_id, prompt_instance))
        prompt_instance_id = cur.fetchone()
        if prompt_instance_id is None:
            cur.execute("INSERT INTO prompt_instance (prompt_template_id, prompt_instance_text, count) VALUES (%s, %s, %s) RETURNING id", (prompt_template_id, prompt_instance, 1))
            prompt_instance_id = cur.fetchone()[0]
        else:
            cur.execute("UPDATE prompt_instance SET count=count+1 WHERE id=%s", (prompt_instance_id[0],))
            prompt_instance_id = prompt_instance_id[0]
        # get example id
        cur.execute("SELECT id FROM examples_example WHERE text=%s", (entity,))
        example_id = cur.fetchone()
        if example_id is None:
            cur.execute("INSERT INTO examples_example (meta, filename, text, created_at, updated_at, project_id, uuid, upload_name, entity_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (json.dumps({}), entity, entity, datetime.datetime.now(), datetime.datetime.now(), 1, str(uuid.uuid4()), entity, entity_type))
            example_id = cur.fetchone()[0]
        else:
            cur.execute("UPDATE examples_example SET updated_at=%s WHERE id=%s", (datetime.datetime.now(), example_id[0]))
            example_id = example_id[0]
        # get prompt example id
        cur.execute("SELECT id FROM prompt_example WHERE prompt_instance_id=%s AND example_id=%s", (prompt_instance_id, example_id))
        prompt_example_id = cur.fetchone()
        if prompt_example_id is None:
            cur.execute("INSERT INTO prompt_example (prompt_instance_id, example_id, count) VALUES (%s, %s, %s) RETURNING id", (prompt_instance_id, example_id, 1))
            prompt_example_id = cur.fetchone()[0]
        else:
            cur.execute("UPDATE prompt_example SET count=count+1 WHERE id=%s", (prompt_example_id[0],))
            prompt_example_id = prompt_example_id[0]

        # retrive prompt template, prompt instance, entity with counts based on entity and entity type
        cur.execute("SELECT prompt_template_text, prompt_instance_text, text, prompt_instance.count, prompt_example.count FROM prompt_template JOIN prompt_instance ON prompt_template.id=prompt_instance.prompt_template_id JOIN prompt_example ON prompt_instance.id=prompt_example.prompt_instance_id JOIN examples_example ON prompt_example.example_id = examples_example.id WHERE examples_example.id=%s AND prompt_template.target_entity_type=%s", (example_id, entity_type))
        
        data = cur.fetchall()
        # transform to dict
        # template, template_count, instance, instance_count
        meta = {"entity_type": entity_type, "count": sum([e[4] for e in data])}
        
        # meta = {"entity_type": entity_type} | {e[0]: {e[1]: {e[2]: {"prompt_instance_count": e[3], "prompt_example_count": e[4]}}} for e in data}
        for e in data:
            if e[0] not in meta:
                meta[e[0]] = {}
            if e[1] not in meta[e[0]]:
                meta[e[0]][e[1]] = {}
            meta[e[0]][e[1]][e[2]] = {"prompt_instance_count": e[3], "prompt_example_count": e[4]}
        # update meta
        cur.execute("UPDATE examples_example SET meta=%s WHERE id=%s", (json.dumps(meta), example_id))



        self.conn.commit()

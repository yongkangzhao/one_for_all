import psycopg
import datetime
import uuid
import json
import pandas as pd
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


"""
-- Table: public.labels_category

-- DROP TABLE IF EXISTS public.labels_category;

CREATE TABLE IF NOT EXISTS public.labels_category
(
    id integer NOT NULL DEFAULT nextval('api_category_id_seq'::regclass),
    prob double precision NOT NULL,
    manual boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    example_id integer NOT NULL,
    label_id integer NOT NULL,
    user_id integer NOT NULL,
    uuid uuid NOT NULL,
    CONSTRAINT api_category_pkey PRIMARY KEY (id),
    CONSTRAINT api_category_example_id_user_id_label_id_25fc0052_uniq UNIQUE (example_id, user_id, label_id),
    CONSTRAINT labels_category_uuid_7ce4d090_uniq UNIQUE (uuid),
    CONSTRAINT api_category_example_id_2dbc87fd_fk_api_example_id FOREIGN KEY (example_id)
        REFERENCES public.examples_example (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_category_label_id_40eb6a8e_fk_api_categorytype_id FOREIGN KEY (label_id)
        REFERENCES public.label_types_categorytype (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_category_user_id_4a62861e_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.labels_category
    OWNER to postgres;
-- Index: api_category_example_id_2dbc87fd

-- DROP INDEX IF EXISTS public.api_category_example_id_2dbc87fd;

CREATE INDEX IF NOT EXISTS api_category_example_id_2dbc87fd
    ON public.labels_category USING btree
    (example_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_category_label_id_40eb6a8e

-- DROP INDEX IF EXISTS public.api_category_label_id_40eb6a8e;

CREATE INDEX IF NOT EXISTS api_category_label_id_40eb6a8e
    ON public.labels_category USING btree
    (label_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_category_user_id_4a62861e

-- DROP INDEX IF EXISTS public.api_category_user_id_4a62861e;

CREATE INDEX IF NOT EXISTS api_category_user_id_4a62861e
    ON public.labels_category USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;
"""
"""
-- Table: public.labels_category

-- DROP TABLE IF EXISTS public.labels_category;

CREATE TABLE IF NOT EXISTS public.labels_category
(
    id integer NOT NULL DEFAULT nextval('api_category_id_seq'::regclass),
    prob double precision NOT NULL,
    manual boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    example_id integer NOT NULL,
    label_id integer NOT NULL,
    user_id integer NOT NULL,
    uuid uuid NOT NULL,
    CONSTRAINT api_category_pkey PRIMARY KEY (id),
    CONSTRAINT api_category_example_id_user_id_label_id_25fc0052_uniq UNIQUE (example_id, user_id, label_id),
    CONSTRAINT labels_category_uuid_7ce4d090_uniq UNIQUE (uuid),
    CONSTRAINT api_category_example_id_2dbc87fd_fk_api_example_id FOREIGN KEY (example_id)
        REFERENCES public.examples_example (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_category_label_id_40eb6a8e_fk_api_categorytype_id FOREIGN KEY (label_id)
        REFERENCES public.label_types_categorytype (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT api_category_user_id_4a62861e_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.labels_category
    OWNER to postgres;
-- Index: api_category_example_id_2dbc87fd

-- DROP INDEX IF EXISTS public.api_category_example_id_2dbc87fd;

CREATE INDEX IF NOT EXISTS api_category_example_id_2dbc87fd
    ON public.labels_category USING btree
    (example_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_category_label_id_40eb6a8e

-- DROP INDEX IF EXISTS public.api_category_label_id_40eb6a8e;

CREATE INDEX IF NOT EXISTS api_category_label_id_40eb6a8e
    ON public.labels_category USING btree
    (label_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: api_category_user_id_4a62861e

-- DROP INDEX IF EXISTS public.api_category_user_id_4a62861e;

CREATE INDEX IF NOT EXISTS api_category_user_id_4a62861e
    ON public.labels_category USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;
"""

class PostgresAPI:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def get_limited_entities(self, entity_type, limit):
        cur = self.conn.cursor()
        
        # cur.execute(f"SELECT text FROM examples_example JOIN labels_category ON examples_example.id=labels_category.example_id WHERE labels_category.label_id IN (SELECT id FROM label_types_categorytype WHERE label_types_categorytype.text = 'Positive') AND examples_example.entity_type = '{entity_type}' LIMIT {limit}")
        # cur.execute(f"SELECT text FROM examples_example  JOIN prompt_example ON examples_example.id = prompt_example.example_id WHERE examples_example.entity_type = '{entity_type}' GROUP BY text ORDER BY count(text) ASC LIMIT {limit}")
        # combine the two queries into one
        cur.execute(f"SELECT text FROM examples_example FULL JOIN labels_category ON examples_example.id=labels_category.example_id FULL JOIN prompt_example ON examples_example.id = prompt_example.example_id WHERE labels_category.label_id IN (SELECT id FROM label_types_categorytype WHERE label_types_categorytype.text = 'Positive') AND examples_example.entity_type = '{entity_type}' GROUP BY text ORDER BY sum(count) ASC LIMIT {limit}")

        rows = cur.fetchall()
        # print(rows)
        return [e[0] for e in rows]

    def check_prompt_exists(self, prompt):
        # check if prompt exists
        cur = self.conn.cursor()
        cur.execute(f"SELECT id FROM prompt_instance WHERE prompt_instance_text = '{prompt}'")
        rows = cur.fetchall()
        return len(rows) > 0

    def prompt_counts(self):
        # sample prompts
        cur = self.conn.cursor()
        cur.execute("SELECT prompt_template_text, sum(count) FROM prompt_instance FULL JOIN prompt_template ON prompt_instance.prompt_template_id = prompt_template.id GROUP BY prompt_template_text ORDER BY sum(count)")
        rows = cur.fetchall()
        return {p[0]:p[1] for p in rows}

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
        # data = [('becoming a [MASK] is...sona] and ', 'becoming a [MASK] is...shady and ', 'victim', 20, 20), ('becoming a [MASK] is...sona] and ', 'becoming a [MASK] is... liar and ', 'victim', 20, 5), ('becoming a [MASK] is...sona] and ', 'becoming a [MASK] is...ardly and ', 'victim', 20, 8), ('becoming a [MASK] is...sona] and ', 'becoming a [MASK] is...itful and ', 'victim', 21, 21)]
        # transform to dict
        # template, template_count, instance, instance_count
        meta = {"entity_type": entity_type}
        
        for e in data:
            if e[0] not in meta:
                meta[e[0]] = {"count": 0}
            if e[1] not in meta[e[0]]:
                meta[e[0]][e[1]] = {}
            meta[e[0]][e[1]][e[2]] = {"count": e[4]}
            meta[e[0]]["count"] += e[4]
        # update meta
        cur.execute("UPDATE examples_example SET meta=%s WHERE id=%s", (json.dumps(meta), example_id))
        

    def get_samples(self, project_name, label=None, limit=None):
        cur = self.conn.cursor()
        query = """
                SELECT  examples_example.entity_type, examples_example.text, examples_example.meta, label_types_categorytype.text as label
                FROM examples_example 
                JOIN labels_category 
                ON examples_example.id=labels_category.example_id 
                JOIN label_types_categorytype
                ON label_types_categorytype.id = labels_category.label_id
                JOIN projects_project
                ON projects_project.id = examples_example.project_id
                """
        if label is not None: query += "WHERE label_types_categorytype.text='%s'"%(label)
        query += "\nAND projects_project.name = '%s'"%(project_name)
        query += """\nAND NOT meta::jsonb ? 'seed'"""
        if limit is not None:
            query += " LIMIT %d" % limit
        cur.execute(query)
        rows = cur.fetchall()

        # create dataframe
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        return df

    def get_sentence_by_entity(self, entity_type, entity_name):
        cur = self.conn.cursor()
        query = "SELECT text FROM public.examples_example WHERE meta->>'entity_type' = '%s' AND meta->>'head' = '%s'"%(entity_type.replace("'","''"), entity_name.replace("'","''"))
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    #db.update_label(i, "Negative")
    def update_label(self, example_id, label_type):
        cur = self.conn.cursor()
        # get label id
        cur.execute("SELECT id FROM label_types_categorytype WHERE text=%s", (label_type,))
        label_type_id = cur.fetchone()
        label_type_id = label_type_id[0]
        # INSERT example label with label type
        cur.execute("INSERT INTO labels_category (prob, manual, created_at, updated_at, example_id, label_id, user_id, uuid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (1.0, True, datetime.datetime.now(), datetime.datetime.now(), example_id, label_type_id, 1, str(uuid.uuid4())))
        # update example meta
        
        # commit
        self.conn.commit()

        
    def get_unlabeled_data(self, project_name, batch_size=10):
        cur = self.conn.cursor()
        query = """
                SELECT examples_example.id, text, meta
                FROM examples_example
                FULL JOIN labels_category
                ON examples_example.id=labels_category.example_id
                JOIN projects_project
                ON projects_project.id = examples_example.project_id
                WHERE label_id is null
                """
        query += "\nAND projects_project.name = '%s'"%(project_name)
        query += """\nAND NOT meta::jsonb ? 'seed'"""
        #order desc
        query += "\nORDER BY examples_example.id DESC"
        cur.execute(query)
        done = False
        while not done:
            rows = cur.fetchmany(batch_size)
            if len(rows) == 0:
                done = True
                continue
            yield pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])



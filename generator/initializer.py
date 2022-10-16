import argparse
import psycopg
import os
import sys
import json
import uuid
import time
from datetime import datetime

def main(args):
    # mongodb
    # print(f"Processing file {args.collection}")
    # with open(args.seed_path+args.collection, "r") as f:
    #     for line in f:
    #         try:
    #             print(line.strip())
    #             data = {
    #                 "value": line.strip(),
    #                 "created_at": datetime.now(),
    #                 "updated_at": datetime.now(),
    #                 "status": "seed",
    #                 "disposition": ["seed"],
    #             }
    #             collection.update_one({"value": line.strip()}, {"$set": data, "$inc":{"count":1}}, upsert=True)
    #         except Exception as e:
    #             print(f"Error: {e}")
    #             print(f"Line: {line}")
    #             continue
    # postgres
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
    #
    print(f"Processing file {args.collection}")
    conn = psycopg.connect(dbname=args.db, user=args.user, password=args.password, host=args.host, port=args.port)
    cur = conn.cursor()
    with open(args.seed_path+args.collection, "r") as f:
        for line in f:
            try:
                print(line.strip())
                query = f"INSERT INTO examples_example (meta, filename, text, created_at, updated_at, project_id, uuid, upload_name, head_type, head, relation, tail_type, tail, entity_type) VALUES ('{{\"seed\": true, \"entity_type\": \"{args.collection}\"}}', 'seed', '{line.strip()}', '{datetime.now()}', '{datetime.now()}', 1, '{uuid.uuid4()}', '{line.strip()}', Null, Null, Null, Null, Null, '{args.collection}');"
                conn.commit()
                cur.execute(query)
                query = f"INSERT INTO labels_category (prob, manual, created_at, updated_at, example_id, label_id, user_id, uuid) VALUES (1.0, True, '{datetime.now()}', '{datetime.now()}', (SELECT id FROM examples_example WHERE text = '{line.strip()}'), (SELECT id FROM label_types_categorytype WHERE text = 'Positive' AND project_id = '1'), 1, '{uuid.uuid4()}');"
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                print(f"Line: {line}")
                conn.rollback()
                continue
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--db", type=str, default="postgres")
    parser.add_argument("--user", type=str, default="postgres")
    parser.add_argument("--password", type=str, default="postgres")
    parser.add_argument("--collection", type=str, required=True)
    parser.add_argument("--seed_path", type=str, default="seeds/")
    args = parser.parse_args()
    main(args)
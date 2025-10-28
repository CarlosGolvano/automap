def get_in_domain(eval_json: dict) -> dict:
    return {
        'entity_coverage': eval_json["entity_coverage"],
        'classes_with_hierarchy': eval_json["classes_with_hierarchy"],
        'predicates_with_hierarchy': eval_json["predicates_with_hierarchy"],
        'single_property_hierarchy_scores': eval_json["single_property_hierarchy_scores"],
        'predicates_direct': eval_json["predicates_direct"],
        'predicates_inverse': eval_json["predicates_inverse"],
        'predicate_details': eval_json["predicate_details"],
    }


def get_common(eval_json: dict) -> dict:
    return {
        # Basic metrics
        'triples': eval_json["triples"],
        'subjects': eval_json["subjects"],
        'subjects_fuzzy': eval_json["subjects_fuzzy"],
        'classes': eval_json["classes"],
        'classes_unique': eval_json["classes_unique"],

        # Property metrics
        'predicates': eval_json["predicates"],
        'predicates_unique': eval_json["predicates_unique"],
        'predicate_datatype_range': eval_json["predicate_datatype_range"],
        'predicate_datatype_range_unique': eval_json["predicate_datatype_range_unique"],

        # Object metrics
        'objects': eval_json["objects"],
        'objects_uris': eval_json["objects_uris"],
        'objects_literals': eval_json["objects_literals"],
    }

from Typing import Dict, Iterable


class BulkUpdateBuilder:

    def __init__(self, model, where_fields, set_fields):
        self.model = model
        self.where_fields = where_fields
        self.set_fields = set_fields
        self.fields = {**where_fields, **set_fields}
        self.stmt_params = []

    def append(self, **kwargs):
        self.stmt_params.append({key: kwargs[key] for key in self.fields})

    def extend(self, values: Iterable[Dict]):
        for value in values:
            self.append(**value)

    def execute(self, db_session):
        stmt = update(self.model).where(
            {field: bindparam(field) for field in self.where_fields}
        ).values(
            {field: bindparam(field) for field in self.set_fields}
        ).execution_options(synchronize_session=False)

        db_session.execute(stmt, self.stmt_params)


bulk_update = BulkUpdateBuilder(
    Order, where_fields=["id"], set_fields=["promotion_id"]
)
buld_update.extend({"id": o.id, "promotion_id": 123} for o in order)

build_update.execute(session)

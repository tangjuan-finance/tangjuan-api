from app.mapper.resource_mapper import ResourceMapper


class ResourceFieldMapper(ResourceMapper):
    @property
    def cid_fields(self):
        return self._get_fields("cid")

    @property
    def association_fields(self):
        return self._get_fields("association")

    def _get_fields(self, field_type: str):
        """Fetches cid or association fields based on the resource type."""
        field_name = f"_{self._resource_type}_{field_type}_fields"
        return getattr(self, field_name)

    _base_cid_fields = frozenset(
        {
            "scenario_id",
        }
    )
    _base_association_fields = frozenset(
        {
            "memo",
        }
    )

    _child_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "child_id",
            }
        )
    )
    _child_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "birth_age",
                "independent_age",
            }
        )
    )

    _asset_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "asset_id",
            }
        )
    )
    _asset_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "max_yearly_return_rate",
                "min_yearly_return_rate",
                "allocation_percentage",
                "start_age",
                "end_age",
            }
        )
    )

    _expense_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "expense_id",
            }
        )
    )
    _expense_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "max_yearly_growth_rate",
                "min_yearly_growth_rate",
                "start_age",
                "end_age",
            }
        )
    )

    _house_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "house_id",
            }
        )
    )
    _house_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "down_payment",
                "interest_rate",
                "loan_term",
                "purchase_age",
                "sale_age",
            }
        )
    )

    _income_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "income_id",
            }
        )
    )
    _income_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "max_yearly_growth_rate",
                "min_yearly_growth_rate",
                "start_age",
                "end_age",
            }
        )
    )

    _liability_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "liability_id",
            }
        )
    )
    _liability_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "interest_rate",
                "allocation_percentage",
                "start_age",
                "end_age",
            }
        )
    )

    _risk_cid_fields = frozenset(
        _base_cid_fields
        | frozenset(
            {
                "risk_id",
            }
        )
    )
    _risk_association_fields = frozenset(
        _base_association_fields
        | frozenset(
            {
                "min_loss",
                "max_loss",
                "start_age",
                "end_age",
            }
        )
    )

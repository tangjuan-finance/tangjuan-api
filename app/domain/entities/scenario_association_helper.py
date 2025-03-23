# from ..associations import (
#     ScenarioExpenseDomain,
#     ScenarioIncomeDomain,
#     ScenarioHouseDomain,
#     ScenarioChildDomain,
#     ScenarioRiskDomain,
#     ScenarioAssetDomain,
#     ScenarioLiabilityDomain,
# )

# class ScenarioAssociationMapper():

#     @classmethod
#     def add_resource(self, scenario, resource_type, resource_instance, **param):
#       if resource_type == "expenses":
#         return self._add_expense(scenario, resource_instance, **param)
#       elif resource_type == "incomes":
#         return self._add_income(scenario, resource_instance, **param)
#       elif resource_type == "houses":
#         return self._add_house(scenario, resource_instance, **param)
#       elif resource_type == "children":
#         return self._add_children(scenario, resource_instance, **param)
#       elif resource_type == "risks":
#         return self._add_risk(scenario, resource_instance, **param)
#       elif resource_type == "assets":
#         return self._add_asset(scenario, resource_instance, **param)
#       elif resource_type == "liabilities":
#         return self._add_liability(scenario, resource_instance, **param)
#       else:
#         raise ValueError(f"Invalid resource type {resource_type}")

#     @classmethod
#     def get_resource(self, scenario, resource_type, resource_instance, **param):
#       pass

#     @classmethod
#     def update_resource(self, scenario, resource_type, resource_instance, **param):
#       pass

#     @classmethod
#     def delete_resource(self, scenario, resource_type, resource_instance, **param):
#       pass

#       # Add Resources
#     def _add_expense(self, scenario, expense, **param):
#       association = ScenarioExpenseDomain(
#         scenario = scenario,
#         expense = expense,
#         **param
#       )

#       scenario.expenses.append(association)

#       return association

#     def _add_income(self, scenario, income, **param):
#       association = ScenarioIncomeDomain(
#         scenario = scenario,
#         income = income,
#         **param
#       )

#       scenario.incomes.append(association)

#       return association

#     def _add_house(self, scenario, house, **param):
#       association = ScenarioHouseDomain(
#         scenario = scenario,
#         house = house,
#         **param
#       )

#       scenario.houses.append(association)

#       return association

#     def _add_child(self, scenario, child, **param):
#       association = ScenarioChildDomain(
#         scenario = scenario,
#         child = child,
#         **param
#       )

#       scenario.children.append(association)

#       return association

#     def _add_risk(self, scenario, risk, **param):
#       association = ScenarioRiskDomain(
#         scenario = scenario,
#         risk = risk,
#         **param
#       )

#       scenario.risks.append(association)

#       return association

#     def _add_asset(self, scenario, asset, **param):
#       association = ScenarioAssetDomain(
#         scenario = scenario,
#         asset = asset,
#         **param
#       )

#       scenario.assets.append(association)

#       return association

#     def _add_liability(self, scenario, liability, **param):
#       association = ScenarioLiabilityDomain(
#         scenario = scenario,
#         liability = liability,
#         **param
#       )

#       scenario.liabilities.append(association)

#       return association

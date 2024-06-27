import numpy as np
from ai_economist.foundation.base.base_component import BaseComponent

class MMTGovernment(BaseComponent):
    name = "MMTGovernment"
    required_entities = ["Labor", "Capital", "Technology", "ForeignTrade"]
    agent_subclasses = ["BasicMobileAgent", "BasicPlanner", "ForeignAgent"]

    def __init__(self, 
                 unemployment_target=0.04, 
                 inflation_target=0.02,
                 initial_money_supply=1000000,
                 govt_spending_multiplier=1.5,
                 base_tax_rate=0.3,
                 progressive_tax_brackets=None,
                 job_guarantee_wage=10,
                 interest_rate=0.02,
                 productivity_growth_rate=0.02,
                 exchange_rate=1.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.unemployment_target = unemployment_target
        self.inflation_target = inflation_target
        self.money_supply = initial_money_supply
        self.govt_spending_multiplier = govt_spending_multiplier
        self.base_tax_rate = base_tax_rate
        self.progressive_tax_brackets = progressive_tax_brackets or {
            50000: 0.2,
            100000: 0.3,
            250000: 0.4,
            500000: 0.5
        }
        self.job_guarantee_wage = job_guarantee_wage
        self.interest_rate = interest_rate
        self.govt_budget = 0
        self.collected_taxes = 0
        self.job_guarantee_spending = 0
        self.govt_debt = 0
        self.private_sector_savings = 0
        self.productivity_growth_rate = productivity_growth_rate
        self.exchange_rate = exchange_rate
        self.inflation_expectations = inflation_target
        self.bank_reserves = 0
        self.foreign_exchange_reserves = 1000000

    def get_additional_state_fields(self, agent_cls_name):
        if agent_cls_name == "BasicMobileAgent":
            return {"money", "labor", "income", "job_guarantee_participant", "savings", "debt", "productivity", "inflation_expectation", "foreign_currency"}
        elif agent_cls_name == "BasicPlanner":
            return {"unemployment_rate", "inflation_rate", "gdp", "gini_coefficient", "govt_debt_to_gdp", "private_savings_to_gdp", "productivity_index", "trade_balance"}
        elif agent_cls_name == "ForeignAgent":
            return {"foreign_currency", "domestic_currency"}
        return set()

    def component_step(self):
        self.update_productivity()
        self.calculate_economic_indicators()
        self.functional_finance()
        self.collect_taxes()
        self.implement_job_guarantee()
        self.manage_interest_rates()
        self.manage_exchange_rate()
        self.distribute_money()
        self.update_private_sector_finances()
        self.update_banking_sector()
        self.handle_international_trade()
        self.update_agent_expectations()

    def update_productivity(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            agent.state["productivity"] *= (1 + self.productivity_growth_rate)

    def calculate_economic_indicators(self):
        total_agents = len(self.world.agents)
        employed_agents = sum(1 for agent in self.world.agents if agent.state["labor"] > 0)
        self.unemployment_rate = 1 - (employed_agents / total_agents)

        total_money = sum(agent.state["money"] for agent in self.world.agents) + self.govt_budget
        self.inflation_rate = (total_money - self.money_supply) / self.money_supply
        self.money_supply = total_money

        self.gdp = sum(agent.state["income"] for agent in self.world.agents)
        
        incomes = sorted(agent.state["income"] for agent in self.world.agents)
        cum_incomes = np.cumsum(incomes)
        equality_dist = np.linspace(0, cum_incomes[-1], len(incomes))
        self.gini_coefficient = (equality_dist - cum_incomes).sum() / cum_incomes.sum()

        self.govt_debt_to_gdp = self.govt_debt / self.gdp if self.gdp > 0 else 0
        self.private_savings_to_gdp = self.private_sector_savings / self.gdp if self.gdp > 0 else 0
        
        self.productivity_index = np.mean([agent.state["productivity"] for agent in self.world.get_agents_of_type("BasicMobileAgent")])
        self.trade_balance = sum([agent.state["foreign_currency"] for agent in self.world.get_agents_of_type("BasicMobileAgent")]) * self.exchange_rate

        planner = self.world.planner
        planner.state["unemployment_rate"] = self.unemployment_rate
        planner.state["inflation_rate"] = self.inflation_rate
        planner.state["gdp"] = self.gdp
        planner.state["gini_coefficient"] = self.gini_coefficient
        planner.state["govt_debt_to_gdp"] = self.govt_debt_to_gdp
        planner.state["private_savings_to_gdp"] = self.private_savings_to_gdp
        planner.state["productivity_index"] = self.productivity_index
        planner.state["trade_balance"] = self.trade_balance

    def functional_finance(self):
        unemployment_gap = self.unemployment_rate - self.unemployment_target
        inflation_gap = self.inflation_rate - self.inflation_target
        productivity_adjustment = (self.productivity_growth_rate - 0.02) * 0.5
        trade_balance_adjustment = -self.trade_balance / self.gdp * 0.1

        spending_adjustment = (unemployment_gap * 2) - (inflation_gap * 1.5) + (self.govt_debt_to_gdp * 0.1) + productivity_adjustment + trade_balance_adjustment
        govt_spending = self.gdp * self.govt_spending_multiplier * (1 + spending_adjustment)

        max_spending = self.gdp * 0.5
        govt_spending = min(govt_spending, max_spending)

        self.create_money(govt_spending)

    def create_money(self, amount):
        self.govt_budget += amount
        self.money_supply += amount
        self.govt_debt += amount

    def collect_taxes(self):
        self.collected_taxes = 0
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            tax_amount = self.calculate_progressive_tax(agent.state["income"])
            agent.state["money"] -= tax_amount
            self.collected_taxes += tax_amount

        self.money_supply -= self.collected_taxes
        self.govt_debt -= self.collected_taxes

    def calculate_progressive_tax(self, income):
        tax = 0
        previous_bracket = 0
        for bracket, rate in sorted(self.progressive_tax_brackets.items()):
            if income > bracket:
                tax += (min(income, bracket) - previous_bracket) * rate
                previous_bracket = bracket
            else:
                break
        tax += (income - previous_bracket) * self.base_tax_rate
        return max(0, tax)

    def implement_job_guarantee(self):
        self.job_guarantee_spending = 0
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["labor"] == 0:
                agent.state["job_guarantee_participant"] = True
                agent.state["money"] += self.job_guarantee_wage
                self.job_guarantee_spending += self.job_guarantee_wage
            else:
                agent.state["job_guarantee_participant"] = False

        self.create_money(self.job_guarantee_spending)

    def manage_interest_rates(self):
        if self.inflation_rate > self.inflation_target and self.unemployment_rate < self.unemployment_target:
            self.interest_rate = min(self.interest_rate + 0.001, 0.1)
        elif self.inflation_rate < self.inflation_target and self.unemployment_rate > self.unemployment_target:
            self.interest_rate = max(self.interest_rate - 0.001, 0.001)
        
        if self.inflation_expectations > self.inflation_target + 0.01:
            self.interest_rate = min(self.interest_rate + 0.002, 0.1)
        elif self.inflation_expectations < self.inflation_target - 0.01:
            self.interest_rate = max(self.interest_rate - 0.002, 0.001)

        self.govt_debt *= (1 + self.interest_rate)

    def manage_exchange_rate(self):
        trade_balance_pressure = self.trade_balance / self.gdp
        interest_rate_differential = self.interest_rate - 0.02
        
        exchange_rate_adjustment = trade_balance_pressure * 0.1 + interest_rate_differential * 0.2
        self.exchange_rate *= (1 + exchange_rate_adjustment)

        if self.exchange_rate < 0.8 or self.exchange_rate > 1.2:
            intervention_amount = (1 - self.exchange_rate) * self.foreign_exchange_reserves * 0.1
            self.foreign_exchange_reserves -= intervention_amount
            self.exchange_rate += intervention_amount / self.foreign_exchange_reserves

    def distribute_money(self):
        total_agents = len(self.world.get_agents_of_type("BasicMobileAgent"))
        spending_per_agent = (self.govt_budget - self.job_guarantee_spending) / total_agents

        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            agent.state["money"] += spending_per_agent

        self.govt_budget = 0

    def update_private_sector_finances(self):
        self.private_sector_savings = 0
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            agent.state["savings"] *= (1 + self.interest_rate)
            agent.state["debt"] *= (1 + self.interest_rate * 1.5)
            self.private_sector_savings += agent.state["savings"]

    def update_banking_sector(self):
        total_deposits = sum([agent.state["savings"] for agent in self.world.get_agents_of_type("BasicMobileAgent")])
        reserve_requirement = 0.1
        self.bank_reserves = total_deposits * reserve_requirement
        loanable_funds = total_deposits - self.bank_reserves

        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["debt"] < agent.state["income"] * 2:
                loan_amount = min(loanable_funds * 0.01, agent.state["income"])
                agent.state["money"] += loan_amount
                agent.state["debt"] += loan_amount
                loanable_funds -= loan_amount

    def handle_international_trade(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if np.random.rand() < 0.1:
                trade_amount = agent.state["money"] * 0.1
                if np.random.rand() < 0.5:
                    agent.state["money"] += trade_amount
                    agent.state["foreign_currency"] += trade_amount / self.exchange_rate
                else:
                    agent.state["money"] -= trade_amount
                    agent.state["foreign_currency"] -= trade_amount / self.exchange_rate

    def update_agent_expectations(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            agent.state["inflation_expectation"] = agent.state["inflation_expectation"] * 0.9 + self.inflation_rate * 0.1

        self.inflation_expectations = np.mean([agent.state["inflation_expectation"] for agent in self.world.get_agents_of_type("BasicMobileAgent")])

    def get_dense_log(self):
        return {
            "unemployment_rate": self.unemployment_rate,
            "inflation_rate": self.inflation_rate,
            "gdp": self.gdp,
            "gini_coefficient": self.gini_coefficient,
            "money_supply": self.money_supply,
            "govt_budget": self.govt_budget,
            "collected_taxes": self.collected_taxes,
            "job_guarantee_spending": self.job_guarantee_spending,
            "govt_debt": self.govt_debt,
            "govt_debt_to_gdp": self.govt_debt_to_gdp,
            "private_savings_to_gdp": self.private_savings_to_gdp,
            "interest_rate": self.interest_rate,
            "productivity_index": self.productivity_index,
            "trade_balance": self.trade_balance,
            "exchange_rate": self.exchange_rate,
            "inflation_expectations": self.inflation_expectations,
            "bank_reserves": self.bank_reserves,
            "foreign_exchange_reserves": self.foreign_exchange_reserves,
        }
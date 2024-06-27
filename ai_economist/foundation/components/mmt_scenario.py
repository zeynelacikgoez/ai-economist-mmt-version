from ai_economist.foundation.base.base_scenario import BaseScenario
from ai_economist.foundation.components.mmt_government import MMTGovernment
from ai_economist.foundation.components.mmt_labor_market import MMTLaborMarket
from ai_economist.foundation.components.continuous_double_auction import ContinuousDoubleAuction
import numpy as np

class MMTScenario(BaseScenario):
    name = "MMTScenario"
    agent_subclasses = ["BasicMobileAgent", "BasicPlanner", "ForeignAgent", "CorporateAgent"]
    required_entities = ["Labor", "Capital", "Technology", "ForeignTrade", "NaturalResources"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.components.extend([
            MMTGovernment(
                unemployment_target=0.04,
                inflation_target=0.02,
                initial_money_supply=1000000,
                govt_spending_multiplier=1.5,
                base_tax_rate=0.3,
                job_guarantee_wage=10,
                interest_rate=0.02,
                productivity_growth_rate=0.02,
                exchange_rate=1.0,
            ),
            MMTLaborMarket(
                base_wage=20,
                skill_premium_factor=1.5,
            ),
            ContinuousDoubleAuction(),  # For simulating financial markets
        ])
        self.commodity_prices = {"oil": 50, "gold": 1500, "wheat": 5}  # Example commodity prices

    def reset_scenario(self):
        super().reset_scenario()
        
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            agent.state.update({
                "money": 1000,
                "labor": 0,
                "income": 0,
                "job_guarantee_participant": False,
                "savings": 0,
                "debt": 0,
                "skill_level": np.random.rand(),
                "employer": None,
                "productivity": 1.0,
                "inflation_expectation": self.get_component("MMTGovernment").inflation_target,
                "foreign_currency": 0,
                "stocks": 0,
                "bonds": 0,
                "commodities": {"oil": 0, "gold": 0, "wheat": 0},
            })

        for agent in self.world.get_agents_of_type("ForeignAgent"):
            agent.state.update({
                "foreign_currency": 10000,
                "domestic_currency": 0,
                "investment_portfolio": {"stocks": 0, "bonds": 0, "commodities": {"oil": 0, "gold": 0, "wheat": 0}},
            })

        for agent in self.world.get_agents_of_type("CorporateAgent"):
            agent.state.update({
                "capital": 100000,
                "employees": [],
                "production": 0,
                "revenue": 0,
                "profit": 0,
                "tax_paid": 0,
            })

    def scenario_step(self):
        super().scenario_step()

        govt = self.get_component("MMTGovernment")
        labor_market = self.get_component("MMTLaborMarket")
        financial_market = self.get_component("ContinuousDoubleAuction")

        self.update_mobile_agents(govt, labor_market)
        self.update_corporate_agents(govt)
        self.handle_international_trade()
        self.simulate_financial_markets(financial_market)
        self.update_commodity_prices()

    def update_mobile_agents(self, govt, labor_market):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["job_guarantee_participant"]:
                agent.state["income"] = govt.job_guarantee_wage
            elif agent.state["labor"] > 0:
                agent.state["income"] = labor_market.calculate_wages(agent)
            else:
                agent.state["income"] = 0

            self.agent_financial_decisions(agent, govt)
            
            agent.state["productivity"] *= (1 + govt.productivity_growth_rate)
            agent.state["inflation_expectation"] = (
                agent.state["inflation_expectation"] * 0.9 + govt.inflation_rate * 0.1
            )

    def agent_financial_decisions(self, agent, govt):
        # Saving and borrowing behavior
        if agent.state["income"] > agent.state["money"]:
            savings = (agent.state["income"] - agent.state["money"]) * 0.1
            agent.state["savings"] += savings
            agent.state["money"] -= savings
        elif agent.state["money"] < 100:
            borrowed = min(100 - agent.state["money"], 50)
            agent.state["debt"] += borrowed
            agent.state["money"] += borrowed

        # Investment decisions
        if agent.state["money"] > 1000:
            investment = (agent.state["money"] - 1000) * 0.2
            agent.state["money"] -= investment
            asset_allocation = np.random.dirichlet(np.ones(3))
            agent.state["stocks"] += investment * asset_allocation[0]
            agent.state["bonds"] += investment * asset_allocation[1]
            commodity_investment = investment * asset_allocation[2]
            for commodity in self.commodity_prices:
                agent.state["commodities"][commodity] += commodity_investment / 3 / self.commodity_prices[commodity]

    def update_corporate_agents(self, govt):
        for agent in self.world.get_agents_of_type("CorporateAgent"):
            agent.state["production"] = sum([employee.state["productivity"] for employee in agent.state["employees"]])
            agent.state["revenue"] = agent.state["production"] * 10  # Simplified revenue calculation
            expenses = sum([employee.state["income"] for employee in agent.state["employees"]])
            agent.state["profit"] = agent.state["revenue"] - expenses
            agent.state["tax_paid"] = govt.calculate_progressive_tax(agent.state["profit"])
            agent.state["capital"] += agent.state["profit"] - agent.state["tax_paid"]

            # Hiring/firing decisions
            if agent.state["profit"] > 0 and len(agent.state["employees"]) < 10:
                self.hire_employee(agent)
            elif agent.state["profit"] < 0 and len(agent.state["employees"]) > 1:
                self.fire_employee(agent)

    def hire_employee(self, corporate_agent):
        unemployed_agents = [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") if agent.state["labor"] == 0]
        if unemployed_agents:
            new_employee = max(unemployed_agents, key=lambda x: x.state["skill_level"])
            new_employee.state["labor"] = 1
            new_employee.state["employer"] = corporate_agent
            corporate_agent.state["employees"].append(new_employee)

    def fire_employee(self, corporate_agent):
        if corporate_agent.state["employees"]:
            fired_employee = min(corporate_agent.state["employees"], key=lambda x: x.state["productivity"])
            fired_employee.state["labor"] = 0
            fired_employee.state["employer"] = None
            corporate_agent.state["employees"].remove(fired_employee)

    def handle_international_trade(self):
        govt = self.get_component("MMTGovernment")
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if np.random.rand() < 0.1:
                trade_amount = agent.state["money"] * 0.1
                if np.random.rand() < 0.5:  # Export
                    agent.state["money"] += trade_amount
                    agent.state["foreign_currency"] += trade_amount / govt.exchange_rate
                else:  # Import
                    agent.state["money"] -= trade_amount
                    agent.state["foreign_currency"] -= trade_amount / govt.exchange_rate

        for foreign_agent in self.world.get_agents_of_type("ForeignAgent"):
            if np.random.rand() < 0.2:
                investment_amount = foreign_agent.state["foreign_currency"] * 0.05
                if np.random.rand() < 0.5:  # Investment in domestic economy
                    foreign_agent.state["foreign_currency"] -= investment_amount
                    foreign_agent.state["domestic_currency"] += investment_amount * govt.exchange_rate
                    self.foreign_investment_allocation(foreign_agent, investment_amount * govt.exchange_rate)
                else:  # Divestment from domestic economy
                    divestment_amount = self.foreign_divestment_allocation(foreign_agent, investment_amount * govt.exchange_rate)
                    foreign_agent.state["domestic_currency"] -= divestment_amount
                    foreign_agent.state["foreign_currency"] += divestment_amount / govt.exchange_rate

    def foreign_investment_allocation(self, foreign_agent, amount):
        allocation = np.random.dirichlet(np.ones(3))
        foreign_agent.state["investment_portfolio"]["stocks"] += amount * allocation[0]
        foreign_agent.state["investment_portfolio"]["bonds"] += amount * allocation[1]
        commodity_investment = amount * allocation[2]
        for commodity in self.commodity_prices:
            foreign_agent.state["investment_portfolio"]["commodities"][commodity] += commodity_investment / 3 / self.commodity_prices[commodity]

    def foreign_divestment_allocation(self, foreign_agent, amount):
        total_investment = sum(foreign_agent.state["investment_portfolio"].values())
        if total_investment == 0:
            return 0
        divestment_amount = min(amount, total_investment)
        for asset_type in foreign_agent.state["investment_portfolio"]:
            if isinstance(foreign_agent.state["investment_portfolio"][asset_type], dict):
                for commodity in foreign_agent.state["investment_portfolio"][asset_type]:
                    foreign_agent.state["investment_portfolio"][asset_type][commodity] *= (1 - divestment_amount / total_investment)
            else:
                foreign_agent.state["investment_portfolio"][asset_type] *= (1 - divestment_amount / total_investment)
        return divestment_amount

    def simulate_financial_markets(self, financial_market):
        # Simplified financial market simulation
        stock_price = financial_market.get_average_price("stock")
        bond_price = financial_market.get_average_price("bond")
        
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if np.random.rand() < 0.1:  # 10% chance of trading
                if np.random.rand() < 0.5:  # Buy
                    if agent.state["money"] > stock_price:
                        agent.state["stocks"] += 1
                        agent.state["money"] -= stock_price
                else:  # Sell
                    if agent.state["stocks"] > 0:
                        agent.state["stocks"] -= 1
                        agent.state["money"] += stock_price

            if np.random.rand() < 0.1:  # 10% chance of trading bonds
                if np.random.rand() < 0.5:  # Buy
                    if agent.state["money"] > bond_price:
                        agent.state["bonds"] += 1
                        agent.state["money"] -= bond_price
                else:  # Sell
                    if agent.state["bonds"] > 0:
                        agent.state["bonds"] -= 1
                        agent.state["money"] += bond_price

    def update_commodity_prices(self):
        for commodity in self.commodity_prices:
            price_change = np.random.normal(0, 0.02)  # Random walk with 2% standard deviation
            self.commodity_prices[commodity] *= (1 + price_change)

    def get_additional_plots(self):
        govt_component = self.get_component("MMTGovernment")
        financial_market = self.get_component("ContinuousDoubleAuction")
        
        plots = {
            "Unemployment and Inflation": {
                "Unemployment Rate": [govt_component.unemployment_rate],
                "Inflation Rate": [govt_component.inflation_rate],
                "Inflation Expectations": [govt_component.inflation_expectations],
            },
            "GDP and Money Supply": {
                "GDP": [govt_component.gdp],
                "Money Supply": [govt_component.money_supply],
                "Productivity Index": [govt_component.productivity_index],
            },
            "Income Inequality": {
                "Gini Coefficient": [govt_component.gini_coefficient],
            },
            "Government Finances": {
                "Collected Taxes": [govt_component.collected_taxes],
                "Job Guarantee Spending": [govt_component.job_guarantee_spending],
                "Government Debt": [govt_component.govt_debt],
                "Government Debt to GDP": [govt_component.govt_debt_to_gdp],
            },
            "Private Sector Finances": {
                "Private Savings to GDP": [govt_component.private_savings_to_gdp],
                "Interest Rate": [govt_component.interest_rate],
                "Bank Reserves": [govt_component.bank_reserves],
            },
            "International Trade": {
                "Trade Balance": [govt_component.trade_balance],
                "Exchange Rate": [govt_component.exchange_rate],
                "Foreign Exchange Reserves": [govt_component.foreign_exchange_reserves],
            },
            "Financial Markets": {
                "Stock Price": [financial_market.get_average_price("stock")],
                "Bond Price": [financial_market.get_average_price("bond")],
            },
            "Commodity Prices": {commodity: [price] for commodity, price in self.commodity_prices.items()},
        }
        
        return plots
from ai_economist.foundation.base.base_component import BaseComponent
import numpy as np

class MMTLaborMarket(BaseComponent):
    name = "MMTLaborMarket"
    required_entities = ["Labor", "Capital", "Technology", "Education"]
    agent_subclasses = ["BasicMobileAgent", "BasicPlanner", "CorporateAgent", "EducationProvider"]

    def __init__(self,
                 base_wage=20,
                 skill_premium_factor=1.5,
                 unemployment_benefits=10,
                 job_search_cost=5,
                 labor_force_participation_rate=0.7,
                 wage_stickiness=0.8,
                 sectors=["Manufacturing", "Services", "Technology"],
                 education_cost=100,
                 education_time=4,
                 automation_rate=0.01,
                 gig_economy_share=0.1,
                 union_strength=0.5,
                 **kwargs):
        super().__init__(**kwargs)
        self.base_wage = base_wage
        self.skill_premium_factor = skill_premium_factor
        self.unemployment_benefits = unemployment_benefits
        self.job_search_cost = job_search_cost
        self.labor_force_participation_rate = labor_force_participation_rate
        self.wage_stickiness = wage_stickiness
        self.sectors = sectors
        self.sector_wages = {sector: base_wage for sector in sectors}
        self.job_openings = {sector: 0 for sector in sectors}
        self.education_cost = education_cost
        self.education_time = education_time
        self.automation_rate = automation_rate
        self.gig_economy_share = gig_economy_share
        self.union_strength = union_strength

    def get_additional_state_fields(self, agent_cls_name):
        if agent_cls_name == "BasicMobileAgent":
            return {"skill_level", "employer", "sector", "job_search_active", "unemployed_duration", 
                    "wage_expectation", "education_level", "education_progress", "gig_worker", "union_member"}
        elif agent_cls_name == "CorporateAgent":
            return {"employees", "sector", "job_openings", "wage_offered", "automation_level"}
        elif agent_cls_name == "EducationProvider":
            return {"students", "courses_offered", "tuition_fees"}
        return set()

    def component_step(self):
        self.update_labor_force_participation()
        self.update_job_openings()
        self.update_automation()
        self.match_jobs()
        self.handle_gig_economy()
        self.calculate_wages()
        self.update_unemployment_duration()
        self.pay_unemployment_benefits()
        self.handle_education()
        self.update_unions()

    def update_labor_force_participation(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            participation_probability = self.labor_force_participation_rate
            if agent.state["education_progress"] > 0:
                participation_probability *= 0.5  # Students are less likely to participate
            if np.random.rand() < participation_probability:
                agent.state["job_search_active"] = True
            else:
                agent.state["job_search_active"] = False
                agent.state["labor"] = 0
                agent.state["employer"] = None
                agent.state["sector"] = None

    def update_job_openings(self):
        self.job_openings = {sector: 0 for sector in self.sectors}
        for corp in self.world.get_agents_of_type("CorporateAgent"):
            sector = corp.state["sector"]
            openings = max(0, corp.state["job_openings"] - len(corp.state["employees"]))
            openings = int(openings * (1 - corp.state["automation_level"]))  # Automation reduces job openings
            self.job_openings[sector] += openings

    def update_automation(self):
        for corp in self.world.get_agents_of_type("CorporateAgent"):
            if np.random.rand() < self.automation_rate:
                corp.state["automation_level"] = min(1, corp.state["automation_level"] + 0.1)

    def match_jobs(self):
        unemployed_agents = [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") 
                             if agent.state["labor"] == 0 and agent.state["job_search_active"]]
        
        for sector in self.sectors:
            sector_openings = self.job_openings[sector]
            sector_applicants = [agent for agent in unemployed_agents 
                                 if agent.state["wage_expectation"] <= self.sector_wages[sector]]
            
            matches = min(sector_openings, len(sector_applicants))
            matched_agents = np.random.choice(sector_applicants, matches, replace=False)
            
            for agent in matched_agents:
                agent.state["labor"] = 1
                agent.state["sector"] = sector
                agent.state["employer"] = self.assign_employer(sector)
                agent.state["unemployed_duration"] = 0
                agent.state["gig_worker"] = False
                unemployed_agents.remove(agent)

        # Update remaining unemployed agents
        for agent in unemployed_agents:
            agent.state["money"] -= self.job_search_cost

    def handle_gig_economy(self):
        gig_workers = np.random.choice(
            [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") if agent.state["labor"] == 0],
            int(len(self.world.get_agents_of_type("BasicMobileAgent")) * self.gig_economy_share),
            replace=False
        )
        for worker in gig_workers:
            worker.state["gig_worker"] = True
            worker.state["labor"] = 0.5  # Part-time work
            worker.state["income"] = self.base_wage * 0.7  # Lower than regular wage

    def calculate_wages(self):
        for sector in self.sectors:
            avg_productivity = np.mean([agent.state["productivity"] 
                                        for agent in self.world.get_agents_of_type("BasicMobileAgent") 
                                        if agent.state["sector"] == sector])
            new_wage = self.base_wage * (1 + avg_productivity * self.skill_premium_factor)
            self.sector_wages[sector] = (self.wage_stickiness * self.sector_wages[sector] + 
                                         (1 - self.wage_stickiness) * new_wage)

        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["labor"] > 0:
                sector = agent.state["sector"]
                wage = self.sector_wages[sector] * (1 + agent.state["skill_level"] * self.skill_premium_factor)
                if agent.state["union_member"]:
                    wage *= (1 + self.union_strength * 0.2)  # Union members get higher wages
                agent.state["income"] = wage
                agent.state["wage_expectation"] = max(agent.state["wage_expectation"], wage)

    def update_unemployment_duration(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["labor"] == 0 and agent.state["job_search_active"]:
                agent.state["unemployed_duration"] += 1
            else:
                agent.state["unemployed_duration"] = 0

    def pay_unemployment_benefits(self):
        govt = self.world.get_component("MMTGovernment")
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["labor"] == 0 and agent.state["job_search_active"]:
                benefit = self.unemployment_benefits * max(0, 1 - agent.state["unemployed_duration"] / 52)  # Benefits decrease over time
                agent.state["money"] += benefit
                govt.create_money(benefit)

    def handle_education(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["education_progress"] > 0:
                agent.state["education_progress"] += 1
                if agent.state["education_progress"] >= self.education_time:
                    agent.state["education_level"] += 1
                    agent.state["education_progress"] = 0
                    agent.state["skill_level"] += 0.2  # Increase skill level upon education completion
            elif agent.state["money"] > self.education_cost and np.random.rand() < 0.1:  # 10% chance to start education
                agent.state["money"] -= self.education_cost
                agent.state["education_progress"] = 1

    def update_unions(self):
        for agent in self.world.get_agents_of_type("BasicMobileAgent"):
            if agent.state["labor"] > 0 and not agent.state["union_member"]:
                if np.random.rand() < self.union_strength * 0.1:  # Chance to join union
                    agent.state["union_member"] = True

    def get_unemployment_rate(self):
        labor_force = [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") 
                       if agent.state["job_search_active"]]
        unemployed = [agent for agent in labor_force if agent.state["labor"] == 0]
        return len(unemployed) / len(labor_force) if labor_force else 0

    def get_labor_force_participation_rate(self):
        all_agents = self.world.get_agents_of_type("BasicMobileAgent")
        labor_force = [agent for agent in all_agents if agent.state["job_search_active"]]
        return len(labor_force) / len(all_agents) if all_agents else 0

    def get_average_wage(self):
        employed_agents = [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") 
                           if agent.state["labor"] > 0]
        if employed_agents:
            return np.mean([agent.state["income"] for agent in employed_agents])
        return 0

    def get_gig_economy_size(self):
        gig_workers = [agent for agent in self.world.get_agents_of_type("BasicMobileAgent") 
                       if agent.state["gig_worker"]]
        return len(gig_workers) / len(self.world.get_agents_of_type("BasicMobileAgent"))

    def get_automation_level(self):
        corps = self.world.get_agents_of_type("CorporateAgent")
        if corps:
            return np.mean([corp.state["automation_level"] for corp in corps])
        return 0

    def get_union_membership_rate(self):
        all_agents = self.world.get_agents_of_type("BasicMobileAgent")
        union_members = [agent for agent in all_agents if agent.state["union_member"]]
        return len(union_members) / len(all_agents) if all_agents else 0

    def get_dense_log(self):
        return {
            "unemployment_rate": self.get_unemployment_rate(),
            "labor_force_participation_rate": self.get_labor_force_participation_rate(),
            "average_wage": self.get_average_wage(),
            "sector_wages": self.sector_wages,
            "job_openings": self.job_openings,
            "gig_economy_size": self.get_gig_economy_size(),
            "automation_level": self.get_automation_level(),
            "union_membership_rate": self.get_union_membership_rate(),
        }
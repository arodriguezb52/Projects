# SSA Period Life Table for Males (example values)
ssa_life_expectancy_male = {
    25: 49.8,
    26: 48.9,
    27: 48.1,
    28: 47.1,
    30: 45.3,
    40: 36.6,
    50: 28.1,
    60: 20.4,
    70: 13.7,
    80: 7.9,
    90: 3.9
}
# SSA Period Life Table for Females (example values)
ssa_life_expectancy_female = {
    25: 55.2,
    26: 54.2,
    27: 53.2,
    28: 52.2,
    30: 50.4,
    40: 41.1,
    50: 32.1,
    60: 23.7,
    70: 16,
    80: 9.4,
    90: 4.7
}


def get_life_expectancy_ssa(age, gender):
    if gender.lower() == 'male':
        life_expectancy_table = ssa_life_expectancy_male    # Indicates the code to what table it should look at
    else:
        life_expectancy_table = ssa_life_expectancy_female

    if age in life_expectancy_table:
        return life_expectancy_table[age]   # Gives the life expectancy value according to age
    else:
        # Looks for the closest life expectancy bracket
        closest_age = max([a for a in life_expectancy_table if a <= age])
        return life_expectancy_table[closest_age]


def robo_advisor():
    while True:
        try:
            # Collect user inputs and checks for invalid user input
            age = int(input("What is your age? "))
            if age <= 0:
                raise ValueError('Age must be a positive integer, Please try again')
            gender = (input("What is your gender (Male/Female)? ")).capitalize()
            if gender not in ['Male', 'Female']:
                raise ValueError('Gender must be either Male or Female, Please try again')
            retirement_age = int(input("At what age do you want to retire? "))
            if retirement_age <= age:
                raise ValueError('Retirement must be greater than your age, Please try again')
            risk_tolerance = input('What is your risk tolerance (Low/Medium/High)?').capitalize()
            if risk_tolerance not in ['Low','Medium','High']:
                raise ValueError('Risk Tolerance has to be Low/Medium/High. Please try again')
            break
        except ValueError as e:
            print(f'Invalid input: {e}. Please try again.')

    # Calculate life expectancy from the SSA Table based on gender
    life_expectancy_remaining = get_life_expectancy_ssa(age, gender)
    life_expectancy = age + life_expectancy_remaining  # Total life expectancy

    year_left = retirement_age - age
    if year_left <= 0:
        return "You are already at or beyond retirement age!"

    # Display life expectancy:
    print(f"Your expected life expectancy is: {life_expectancy} years.")
    print(f"Based on the SSA table, you have {life_expectancy_remaining} years remaining")

    allocation = asset_allocation(year_left,risk_tolerance)

    print(f'\nAsset Allocation for {year_left} years left until retirement with {risk_tolerance} risk tolerance: ')
    for asset, percentage in allocation.items():
        print(f'{asset}: {percentage * 100:.2f}%')


def asset_allocation(years_left,risk_tolerance):
    if years_left > 30:
        allocation = {"US Equity": .50, "International Equity": .20, "Real Estate": .20, "Fixed Income": .10}
    elif 20 <= years_left <= 30:
        allocation = {"US Equity": .45, "International Equity": .15, "Real Estate": .20, "Fixed Income": .20}
    elif 10 <= years_left < 20:
        allocation = {"US Equity": .40, "International Equity": .15, "Real Estate": .15, "Fixed Income": .30}
    elif 5 <= years_left < 10:
        allocation = {"US Equity": .35, "International Equity": .10, "Real Estate": .15, "Fixed Income": .40}
    else:
        allocation = {"US Equity": .30, "International Equity": .10, "Real Estate": .10, "Fixed Income": .50}

    if risk_tolerance == "Low":
        allocation['US Equity'] *= 0.2
        allocation['International Equity'] *= 0.2
        allocation['Fixed Income'] *= 1.8
    elif risk_tolerance == 'High':
        allocation['US Equity'] *= 1.05
        allocation['International Equity'] *= 1.05
        allocation['Fixed Income'] *= .5

    total_percentage = sum(allocation.values())
    allocation = {k:v / total_percentage for k, v in allocation.items()}

    return allocation

robo_advisor()

import requests
import pprint
import pandas as pd

# using python request module to interact with the Edamam Search Recipe REST API
def search_recipe(ingredient, meal_type):
    #setting API key and ID
    app_id = 'adc26e15'
    app_key = '3dc4d461a603a76bb8d7d688f5a8c5fb'

    #setting the url params that will be included in the request
    params = {"q": ingredient,  "mealType": meal_type}
    url = f'https://api.edamam.com/api/recipes/v2?type=public&app_id={app_id}&app_key={app_key}'
    result = requests.get(url, params)
    search_data = result.json()
    return search_data['hits']


def show_results():
    #ask user for input information
    ingredient = input("Please enter one ingredient (e.g. 'Chicken')")
    max_no_of_calories = float(input('Enter the max amount of calories desired in recipe: '))
    meal_type = input("Please enter the desired meal type of the day (e.g 'Dinner', 'Lunch', 'Breakfast', 'Snack', "
                      "'Teatime')").lower()

    #creating an empty list used to append the search results
    data_label = []
    data_uri = []
    data_calories = []
    # run the request using the user input and save results
    results = search_recipe(ingredient, meal_type)

    # check if result list is empty
    if len(results) > 0:

        # for each result pprint each recipe details
        for result in results:
            recipe = result['recipe']
            if recipe['calories'] < max_no_of_calories:

                # save recipe details
                recipe_title = (result["recipe"]["label"])
                image = (result["recipe"]["image"])
                calories = (round(result["recipe"]["calories"]))
                meal_type_result = (result["recipe"]["mealType"])
                link_recipe = (result["recipe"]["url"])

                # print recipe details
                print(f'\n Recipe Title:{recipe_title} \n')
                print(f'Recipe Image: {image}')
                print(f'Total of Calories: {calories}. Meal Type: {meal_type_result}')
                pprint.pprint(result["recipe"]["ingredientLines"])
                print(f'Link for the full recipe: {link_recipe} \n')

                # for each result we append the label, url and calories to the empty data list declared above
                data_label.append(recipe_title)
                data_uri.append(link_recipe)
                data_calories.append(calories)

                # creating a data dictionary used to save the data inside a csv file - the keys will be the column heads
                # and the values will be the appended data from each recipe result
            data = {'Label': data_label,
                    'URL': data_uri,
                    'No of Calories': data_calories
                    }

            # using the pandas library and pd.DataFrame command we create a dataframe
            #a dataframe is a 2 dimensional data structure, like a table with rows and columns
            df = pd.DataFrame(data, columns=['Label', 'URL', 'No of Calories'])

            # using df.to_csv() function which converts DataFrame into CSV data
            df.to_csv(r'/Users/cecil/PycharmProjects/cfg-python/team.csv',
                      index=False, header=True)
            # if no recipes are found matching the user's criteria then an error message is printed
    else:
        print("We could not find any recipes that match your criteria. Please try again!")


show_results()


def sort_recipes():
    # the pd.read_csv() function takes a path to a csv file and reads the data into a Pandas DataFrame object
    df2 = pd.read_csv(r'/Users/cecil/PycharmProjects/cfg-python/Python-cfg-project/recipes.csv')

    # sorting the values in ascending order by number of calories
    sorted_df = df2.sort_values(by=["No of Calories"], ascending=True)

    # save ordered data into csv file
    sorted_df.to_csv(r'Users/cecil/PycharmProjects/cfg-python/Python-cfg-project/recipes.csv', index=False)


sort_recipes()

from django.db import models
from datetime import datetime

# Create your models here.

class Ingredients(models.Model):
    # name, no real restrictions
    ingredient_name = models.CharField(max_length=50)
    # both quant and price_per_unit should be positive, right? I'd be open to quant being negative
    quantity = models.FloatField(default=0)
    price_per_unit = models.FloatField(default=0)
    units = models.CharField(max_length=50)  # unsaved! e.g. "oz", "mL"

    def __str__(self):
        # it's good practice
        return f"{self.ingredient_name} - {self.quantity} {self.units}"
    
    def get_absolute_url(self):
        return '..'

class MenuItems(models.Model):
    # descriptions
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=50, default='')  # not required
    # numerical, following the Ingredients field choice
    item_price = models.FloatField(default=0)

    def __str__(self):
        if self.item_description != '':
            return self.item_name
        else:
            return self.item_name + '\n' + self.item_description

    def get_absolute_url(self):
        return '..'

class RecipeRequirements(models.Model):
    # this should self-delete upon deletion of MenuItems or Ingredients
    '''
    probably just foreign keys for both, right? That's it?
    Okay, so yeah - this class is here specifically to avoid the ManyToManyField, it seems
    '''
    # per the guide, it appears that you create one requirement object per menu_item/ingredient
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    ingredient_quantity = models.FloatField(default=0)  # can I skip this? If not...how do I implement correctly?

    def __str__(self):
        return f'menu item: {self.menu_item.item_name}' + '\n' + f'ingredient: {self.ingredient.ingredient_name}'
    
    def get_absolute_url(self):
        return '..'

# optionally, could create "sub-orders" here, which I pass to Purchase to close out full tabs

class Purchase(models.Model):
    '''
    probably need an "update that external field" method
    as well as foreign keys - but no "delete on"

    simplifying assumption: I'll take one menu item and a quantity at a time
    '''
    # basic metadata
    customer_name = models.CharField(max_length=50)
    purchase_timestamp = models.DateField(default=datetime.now())  # temp: default = now

    # now I need to add the menu items and their quants...hm...
    # I think I could sloppily ad-hoc it here, or define it in MenuItems as a param
    #ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)  # alternative to Cascade here?
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField(default=0)
    #recipe_requirements = models.ForeignKey(RecipeRequirements, on_delete=models.CASCADE)

    # output
    purchase_price = models.FloatField(default=0)

    def purchase(self):
        # set time
        self.purchase_timestamp = datetime.now()
        # update total
        self.purchase_price += self.menu_item.item_price * self.order_quantity

        # inventory - I'll have to add this later, brutal to test now
        '''
        how do I call the recipe requirements w/o passing it as a param when creating the object?

        something like:
        for req in (find recipe req that matches item menu):
            update item inventory
        
        should I/can I handle this from within recipeRequirements? If so, how do I call those?
        I honestly might have to handle this in views somehow, let's pause for now
        '''
        return
    
    def __str__(self):
        receipt_string = '''{0}
        {1}
        {2} - {3}
        {4}'''.format(self.customer_name, self.purchase_timestamp, self.menu_item,
                      self.order_quantity, self.purchase_price)
        return receipt_string

    def get_absolute_url(self):
        return '..'


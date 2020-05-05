
class Item:
    def __init__(self, day, name, price, count):
        self.day = day
        self.name = name
        self.price = price
        self.count = count
        self.total_cost = int(price * 10 * count)
        self.total_reward = 1000 * count + (day + 30) * count - self.total_cost


class ItemWithSlots(Item):
    __slots__ = 'day', 'name', 'price', 'count', 'total_cost', 'total_reward'


class Investor:
    def __init__(self, n_days, m_items, s_money):
        self.n_days = n_days
        self.m_items = m_items
        self.s_money = s_money

        self.items = []
        self.total_reward = None

    def add_item_or_not(self, item):
        if self.s_money - item.total_cost >= 0:
            self.items.append(item)
            self.s_money -= item.total_cost

    def add_item(self, item):
        self.items.append(item)

    def get_total_reward(self):
        if self.total_reward is not None:
            return self.total_reward
        total_reward = 0
        for item in self.items:
            total_reward += item.total_reward
        return total_reward



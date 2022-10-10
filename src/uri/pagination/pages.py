"""Информации о страницах данных REST API."""

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class Page(BaseModel):
    """Запрашиваемая клиентом REST API страница данных."""

    number: PositiveInt
    size: PositiveInt

    @property
    def limit(self) -> PositiveInt:
        """Максимум элементов на странице.

        Returns:
            self.size.
        """
        return self.size

    @property
    def offset(self) -> NonNegativeInt:
        """Индекс первого элемента этой страницы.

        Подразумевается индекс в разбиваемом на странице списке элементов.

        Returns:
            Номер индекса.
        """
        return self.size * (self.number - 1)


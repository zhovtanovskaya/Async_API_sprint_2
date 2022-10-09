"""Кэширование результатов для HTTP-запросов в Redis."""

import logging
import pickle
from functools import wraps
from typing import Any, Callable, Iterable

from db.redis import get_redis

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class RedisCache:
    """Кэшировать результат работы функции-контроллера в Redis.

    Чтобы использовать этот декоратор, обязательно указывать его
    первым снизу среди декораторов:
    @get(...)
    @RedisCache(...)
    def path_operation_function(...): ...

    Ключ для хранения результата работы контроллера в кэше
    -- это сигнатура вызова контроллера.  В сигнатуру не включаются
    параметры из self.exclude_kwargs.

    Значение для Redis сериализуется pickle.
    """

    def __init__(self, exclude_kwargs: Iterable[str]):
        """Инициализировать декоратор.

        Args:
            exclude_kwargs: Имена параметров контроллера, которые не нужно
                включать в ключ кэша.
        """
        self.exclude_kwargs = exclude_kwargs

    def __call__(self, path_func: Callable) -> Callable:
        """Заключить path_func в обертку, которая будет кэшировать результаты.

        Args:
            path_func: Декорируемый контроллер.

        Returns:
            Обертка, которая сохраняет и достает из кэша результаты path_func.
        """
        @wraps(path_func)
        async def caching_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Доставать и сохранять результат работы контроллера в Redis.

            Args:
                args: Позиционные аргументы контроллера.
                kwargs: Ключевые аргументы контроллера.

            Returns:
                Результат работы контроллера либо вычисленный, либо из Redis.
            """
            redis = await get_redis()
            key = _get_func_signature(
                path_func, args, kwargs, self.exclude_kwargs)
            cached_result = await redis.get(key)
            if cached_result:
                logging.info('Extracted results from cache for %s. ', key)
                return pickle.loads(cached_result)
            result = await path_func(*args, **kwargs)
            await redis.set(
                key, pickle.dumps(result), expire=CACHE_EXPIRE_IN_SECONDS,
            )
            return result
        return caching_wrapper


def _get_func_signature(
        func: Callable,
        args: tuple[Any],
        kwargs: dict,
        exclude_kwargs: Iterable[str],
        ) -> str:
    """Сформировать строку вызова функции с аргументами.

    Args:
        func: Функция.
        args: Позиционные аргументы функции.
        kwargs: Ключевые аргументы функции.
        exclude_kwargs: Ключевые аргументы, которые нужно убрать из сигнатуры.

    Returns:
        Сигнатура функции path_func в виде строки
    """
    key_kwargs = dict(kwargs)
    for kwarg_name in exclude_kwargs:
        del key_kwargs[kwarg_name]
    return f'{func.__module__}.{func.__name__}(*{args}, **{key_kwargs})'


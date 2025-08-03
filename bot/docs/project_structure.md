# Project Structure

- `/bot`

  The package is the main.

- `/bot/assets`

  The directory contains images, fonts, medias, ect.

- `/bot/cogs`

  The package contains cog files.

- `/bot/cogs/template_cog`

  The package contains some modules for cog.

- `/bot/cogs/template_cog/cog.py`

  The file contains class which inherits from `commands.Cog`.

- `/bot/cogs/template_cog/views.py`

  The file contains classes which inherits from `disnake.ui.View`.

- `/bot/cogs/template_cog/modals.py`

  The file contains classes which inherits from `disnake.ui.Modal`.

- `/bot/cogs/template_cog/embeds.py`

  The file contains frequently used objects of `disnake.Embed`. Every variable in this file - lambda function, which returns object of `disnake.Embed`.

- `/bot/core`

  The package contains modules required for the operation of cogs.

- `/bot/core/database.py`

  The file contains sqlalchemy objects for database interaction.

- `/bot/core/utils.py`

  The file contains utility functions.

- `/bot/core/logger.py`

  The file contains object `logger` of `logging.Logger`. Using for logging.

- `/bot/core/configuration.py`

  The file contains bot configuration. More information about configuration [here](./project_configuration.md).

- `/bot/core/models`

  The package contains files with class inherits from `sqlalchemy.Model` inside.

- `/bot/core/models/example_model.py`

  The package contains files with class inherits from `sqlalchemy.Model` inside.

- `/bot/docs`

  The package contains project documentation.

- `/bot/services`

  The package contains services. All business logic happens in services.

- `/bot/services/example_service`

  The package contains service. It is allowed to create additional files for the operation of this particular service.

- `/bot/services/example_service/service.py`

  The file contains a service class, the class should be named is like service in common.

- `/bot/migrations`

  Alembic migrations.

- `/bot/logs`

  The package contains bot log files.
"""
    <!!! WRITE A REALLY GOOD DOCSTRING !!!>
"""
# pylint: disable=W1202,C0111

"""

# ########################################################### #

            Method A - A separate thread for sources.


    * A custom source must follow strict naming convention.
    * A custom source must be named CustomNameExoEdgeSource.
    * A custom source must subclass ExoEdgeSource unless using
      the "classic" 'from module import function' style where
      ExoEdge will just import your installed module and call
      your functions with parameters and positionals.

      E.g.

      # my_module.py

      def my_function(*positionals, **parameters):
          pass

    The rest of the code below can be used as a starting point
    for your custom source.

    A more complete example can be found in:

        github.com/exosite/exoedge_developer_guide
"""

# ########################################################### #

from exoedge.sources import ExoEdgeSource
from exoedge_simulator.exoedge_simulator import SimulatorExoEdgeSource



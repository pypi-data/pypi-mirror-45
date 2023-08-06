import numpy as np
from scipy.integrate import quad

from autofit.tools.dimension_type import map_types
from autolens.model import dimensions as dim
from autolens.model.profiles import geometry_profiles


class LightProfile(object):
    """Mixin class that implements functions common to all light profiles"""

    def intensities_from_grid_radii(self, grid_radii):
        """
        Abstract method for obtaining intensity at on a grid of radii.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        raise NotImplementedError("intensity_at_radius should be overridden")

    # noinspection PyMethodMayBeStatic
    def intensities_from_grid(self, grid, grid_radial_minimum=None):
        """
        Abstract method for obtaining intensity at a grid of Cartesian (y,x) coordinates.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        Returns
        -------
        intensity : ndarray
            The value of intensity at the given radius
        """
        raise NotImplementedError("intensity_from_grid should be overridden")

    def luminosity_within_circle_in_units(self, radius):
        raise NotImplementedError()

    def luminosity_within_ellipse_in_units(self, major_axis):
        raise NotImplementedError()


# noinspection PyAbstractClass
class EllipticalLightProfile(geometry_profiles.EllipticalProfile, LightProfile):
    """Generic class for an elliptical light profiles"""

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0):
        """  Abstract class for an elliptical light-profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        """
        super(EllipticalLightProfile, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi)

    def luminosity_within_circle_in_units(self, radius: dim.Length, unit_luminosity='eps', kpc_per_arcsec=None,
                                          exposure_time=None):
        """Integrate the light profile to compute the total luminosity within a circle of specified radius. This is \
        centred on the light profile's centre.

        The following units for mass can be specified and output:

        - Electrons per second (default) - 'eps'.
        - Counts - 'counts' (multiplies the luminosity in electrons per second by the exposure time).

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float or None
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """

        if not isinstance(radius, dim.Length):
            radius = dim.Length(value=radius, unit_length='arcsec')

        profile = self.new_profile_with_units_converted(unit_length=radius.unit_length, unit_luminosity=unit_luminosity,
                                                        kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time)

        luminosity = quad(profile.luminosity_integral, a=0.0, b=radius, args=(1.0,))[0]
        return dim.Luminosity(luminosity, unit_luminosity)

    def luminosity_within_ellipse_in_units(self, major_axis, unit_luminosity='eps', kpc_per_arcsec=None,
                                           exposure_time=None):
        """Integrate the light profiles to compute the total luminosity within an ellipse of specified major axis. \
        This is centred on the light profile's centre.

        The following units for mass can be specified and output:

        - Electrons per second (default) - 'eps'.
        - Counts - 'counts' (multiplies the luminosity in electrons per second by the exposure time).

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float or None
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """

        if not isinstance(major_axis, dim.Length):
            major_axis = dim.Length(major_axis, 'arcsec')

        profile = self.new_profile_with_units_converted(unit_length=major_axis.unit_length,
                                                        unit_luminosity=unit_luminosity,
                                                        kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time)
        luminosity = quad(profile.luminosity_integral, a=0.0, b=major_axis, args=(self.axis_ratio,))[0]
        return dim.Luminosity(luminosity, unit_luminosity)

    def luminosity_integral(self, x, axis_ratio):
        """Routine to integrate the luminosity of an elliptical light profile.

        The axis ratio is set to 1.0 for computing the luminosity within a circle"""
        r = x * axis_ratio
        return 2 * np.pi * r * self.intensities_from_grid_radii(x)


class EllipticalGaussian(EllipticalLightProfile):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 sigma: dim.Length = 0.01):
        """ The elliptical Gaussian light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        sigma : float
            The full-width half-maximum of the Gaussian.
        """
        super(EllipticalGaussian, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi)

        self.intensity = intensity
        self.sigma = sigma

    def intensities_from_grid_radii(self, grid_radii):
        """Calculate the intensity of the Gaussian light profile on a grid of radial coordinates.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        return np.multiply(np.divide(self.intensity, self.sigma * np.sqrt(2.0 * np.pi)),
                           np.exp(-0.5 * np.square(np.divide(grid_radii, self.sigma))))

    @geometry_profiles.transform_grid
    @geometry_profiles.move_grid_to_radial_minimum
    def intensities_from_grid(self, grid, grid_radial_minimum=None):
        """
        Calculate the intensity of the light profile on a grid of Cartesian (y,x) coordinates.

        If the coordinates have not been transformed to the profile's geometry, this is performed automatically.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        return self.intensities_from_grid_radii(self.grid_to_elliptical_radii(grid))


class SphericalGaussian(EllipticalGaussian):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 intensity: dim.Luminosity = 0.1,
                 sigma: dim.Length = 0.01):
        """ The spherical Gaussian light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        sigma : float
            The full-width half-maximum of the Gaussian.
        """
        super(SphericalGaussian, self).__init__(centre=centre, axis_ratio=1.0, phi=0.0, intensity=intensity,
                                                sigma=sigma)


class AbstractEllipticalSersic(EllipticalLightProfile):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6,
                 sersic_index: float = 4.0):
        """ Abstract base class for an elliptical Sersic light profile, used for computing its effective radius and
        Sersic constant.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        intensity : float
            Overall intensity normalisation in the light profiles (electrons per second)
        effective_radius : float
            The circular radius containing half the light of this model_mapper
        sersic_index : Int
            Controls the concentration of the of the profile (lower value -> less concentrated, \
            higher value -> more concentrated).
        """
        super(AbstractEllipticalSersic, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi)
        self.intensity = intensity
        self.effective_radius = effective_radius
        self.sersic_index = sersic_index

    def new_profile_with_units_distance_converted(self, units_distance, kpc_per_arcsec=None):
        self.units_distance = units_distance
        self.centre = self.centre.convert(unit_distance=units_distance, kpc_per_arcsec=kpc_per_arcsec)
        self.effective_radius = self.effective_radius.convert(unit_distance=units_distance,
                                                              kpc_per_arcsec=kpc_per_arcsec)
        return self

    @property
    def elliptical_effective_radius(self):
        """The effective_radius of a Sersic light profile is defined as the circular effective radius. This is the \
        radius within which a circular aperture contains half the profiles's total integrated light. For elliptical \
        systems, this won't robustly capture the light profile's elliptical shape.

        The elliptical effective radius instead describes the major-axis radius of the ellipse containing \
        half the light, and may be more appropriate for highly flattened systems like disk galaxies."""
        return self.effective_radius / np.sqrt(self.axis_ratio)

    @property
    def sersic_constant(self):
        """ A parameter derived from Sersic index which ensures that effective radius contains 50% of the profile's
        total integrated light.
        """
        return (2 * self.sersic_index) - (1. / 3.) + (4. / (405. * self.sersic_index)) + (
                46. / (25515. * self.sersic_index ** 2)) + (131. / (1148175. * self.sersic_index ** 3)) - (
                       2194697. / (30690717750. * self.sersic_index ** 4))

    def intensity_at_radius(self, radius):
        """ Compute the intensity of the profile at a given radius.

        Parameters
        ----------
        radius : float
            The distance from the centre of the profile.
        """
        return self.intensity * np.exp(
            -self.sersic_constant * (((radius / self.effective_radius) ** (1. / self.sersic_index)) - 1))


class EllipticalSersic(AbstractEllipticalSersic, EllipticalLightProfile):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6,
                 sersic_index: float = 4.0):
        """ The elliptical Sersic light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concentration of the of the profile (lower value -> less concentrated, \
            higher value -> more concentrated).
        """
        super(EllipticalSersic, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi, intensity=intensity,
                                               effective_radius=effective_radius, sersic_index=sersic_index)

    def intensities_from_grid_radii(self, grid_radii):
        """
        Calculate the intensity of the Sersic light profile on a grid of radial coordinates.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        np.seterr(all='ignore')
        return np.multiply(self.intensity, np.exp(
            np.multiply(-self.sersic_constant,
                        np.add(np.power(np.divide(grid_radii, self.effective_radius), 1. / self.sersic_index), -1))))

    @geometry_profiles.transform_grid
    @geometry_profiles.move_grid_to_radial_minimum
    def intensities_from_grid(self, grid, grid_radial_minimum=None):
        """ Calculate the intensity of the light profile on a grid of Cartesian (y,x) coordinates.

        If the coordinates have not been transformed to the profile's geometry, this is performed automatically.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        return self.intensities_from_grid_radii(self.grid_to_eccentric_radii(grid))


class SphericalSersic(EllipticalSersic):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6,
                 sersic_index: float = 4.0):
        """ The spherical Sersic light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concentration of the of the light profile.
        """
        super(SphericalSersic, self).__init__(centre=centre, axis_ratio=1.0, phi=0.0, intensity=intensity,
                                              effective_radius=effective_radius, sersic_index=sersic_index)


class EllipticalExponential(EllipticalSersic):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6):
        """ The elliptical exponential profile.

        This is a subset of the elliptical Sersic profile, specific to the case that sersic_index = 1.0.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second centre of the light profile.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        """
        super(EllipticalExponential, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi, intensity=intensity,
                                                    effective_radius=effective_radius, sersic_index=1.0)


class SphericalExponential(EllipticalExponential):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6):
        """ The spherical exponential profile.

        This is a subset of the elliptical Sersic profile, specific to the case that sersic_index = 1.0.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        """
        super(SphericalExponential, self).__init__(centre=centre, axis_ratio=1.0, phi=0.0, intensity=intensity,
                                                   effective_radius=effective_radius)


class EllipticalDevVaucouleurs(EllipticalSersic):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6):
        """ The elliptical Dev Vaucouleurs light profile.

        This is a subset of the elliptical Sersic profile, specific to the case that sersic_index = 4.0.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        """
        super(EllipticalDevVaucouleurs, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi,
                                                       intensity=intensity, effective_radius=effective_radius,
                                                       sersic_index=4.0)


class SphericalDevVaucouleurs(EllipticalDevVaucouleurs):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6):
        """ The spherical Dev Vaucouleurs light profile.

        This is a subset of the elliptical Sersic profile, specific to the case that sersic_index = 1.0.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        """
        super(SphericalDevVaucouleurs, self).__init__(centre=centre, axis_ratio=1.0, phi=0.0, intensity=intensity,
                                                      effective_radius=effective_radius)


class EllipticalCoreSersic(EllipticalSersic):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 axis_ratio: float = 1.0,
                 phi: float = 0.0,
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6,
                 sersic_index: float = 4.0,
                 radius_break: dim.Length = 0.01,
                 intensity_break: dim.Luminosity = 0.05,
                 gamma: float = 0.25,
                 alpha: float = 3.0):
        """ The elliptical cored-Sersic light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concentration of the of the profile (lower value -> less concentrated, \
            higher value -> more concentrated).
        radius_break : Float
            The break radius separating the inner power-law (with logarithmic slope gamma) and outer Sersic function.
        intensity_break : Float
            The intensity at the break radius.
        gamma : Float
            The logarithmic power-law slope of the inner core profiles
        alpha :
            Controls the sharpness of the transition between the inner core / outer Sersic profiles.
        """
        super(EllipticalCoreSersic, self).__init__(centre=centre, axis_ratio=axis_ratio, phi=phi, intensity=intensity,
                                                   effective_radius=effective_radius, sersic_index=sersic_index)
        self.radius_break = radius_break
        self.intensity_break = intensity_break
        self.alpha = alpha
        self.gamma = gamma

    def new_profile_with_units_distance_converted(self, units_distance, kpc_per_arcsec=None):
        self.units_distance = units_distance
        self.centre = self.centre.convert(unit_distance=units_distance, kpc_per_arcsec=kpc_per_arcsec)
        self.effective_radius = self.effective_radius.convert(unit_distance=units_distance,
                                                              kpc_per_arcsec=kpc_per_arcsec)
        self.radius_break = self.radius_break.convert(unit_distance=units_distance, kpc_per_arcsec=kpc_per_arcsec)
        return self

    @property
    def intensity_prime(self):
        """Overall intensity normalisation in the rescaled Core-Sersic light profiles (electrons per second)"""
        return self.intensity_break * (2.0 ** (-self.gamma / self.alpha)) * np.exp(
            self.sersic_constant * (((2.0 ** (1.0 / self.alpha)) * self.radius_break) / self.effective_radius) ** (
                    1.0 / self.sersic_index))

    def intensities_from_grid_radii(self, grid_radii):
        """Calculate the intensity of the cored-Sersic light profile on a grid of radial coordinates.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        return np.multiply(np.multiply(self.intensity_prime, np.power(
            np.add(1, np.power(np.divide(self.radius_break, grid_radii), self.alpha)), (self.gamma / self.alpha))),
                           np.exp(np.multiply(-self.sersic_constant,
                                              (np.power(np.divide(np.add(np.power(grid_radii, self.alpha), (
                                                      self.radius_break ** self.alpha)),
                                                                  (self.effective_radius ** self.alpha)), (
                                                                1.0 / (self.alpha * self.sersic_index)))))))


class SphericalCoreSersic(EllipticalCoreSersic):

    @map_types
    def __init__(self,
                 centre: dim.Position = (0.0, 0.0),
                 intensity: dim.Luminosity = 0.1,
                 effective_radius: dim.Length = 0.6,
                 sersic_index: float = 4.0,
                 radius_break: dim.Length = 0.01,
                 intensity_break: dim.Luminosity = 0.05,
                 gamma: float = 0.25,
                 alpha: float = 3.0):
        """ The elliptical cored-Sersic light profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concentration of the of the profile (lower value -> less concentrated, \
            higher value -> more concentrated).
        radius_break : Float
            The break radius separating the inner power-law (with logarithmic slope gamma) and outer Sersic function.
        intensity_break : Float
            The intensity at the break radius.
        gamma : Float
            The logarithmic power-law slope of the inner core profiles
        alpha :
            Controls the sharpness of the transition between the inner core / outer Sersic profiles.
        """
        super(SphericalCoreSersic, self).__init__(centre=centre, axis_ratio=1.0, phi=0.0, intensity=intensity,
                                                  effective_radius=effective_radius, sersic_index=sersic_index,
                                                  radius_break=radius_break, intensity_break=intensity_break,
                                                  gamma=gamma, alpha=alpha)
        self.radius_break = radius_break
        self.intensity_break = intensity_break
        self.alpha = alpha
        self.gamma = gamma
